import os, shutil, time, datetime, csv, sys
from config import *
from scraper import *
import pandas as pd
from pypdf import PdfReader

def downloadBatch(parentPath, trackingNum):
    
    batchPath = os.path.join(parentPath, trackingNum)
    # make inner folder with name of tracking number (if not exists)
    if not os.path.exists(batchPath): os.makedirs(batchPath)
    os.chdir(batchPath)

    print(f"Downloading batch {trackingNum}...")
    # download each batch
    try: filingInfo = runScraper(trackingNum, DRIVER_PATH)
    except: return None # Invalid filing number
    
    # move into corresponding folder
    for file in os.listdir(DOWNLOADS_PATH):
        src = os.path.join(DOWNLOADS_PATH, file).replace("\\", "/")
        dest = os.path.join(batchPath, file).replace("\\", "/")
        
        # If file was created a minute or less ago, it is moved from the DOWNLOADS_PATH to the DESTINATION_PATH
        creation = datetime.datetime.fromtimestamp(os.stat(src).st_ctime)
        now = datetime.datetime.now()
        if creation >= now - datetime.timedelta(minutes=1):
            shutil.move(src, dest) # move file
    
    print(f"Downloading filing info for {trackingNum}...")
    # save filing info as .csv
    csvPath = os.path.join(batchPath, 'filing_info.csv')
    with open(csvPath, 'w', newline='') as f:
        writer = csv.writer(f)
        for label, value in filingInfo.items():
            writer.writerow([label, value])
    print("\nFinished.")
    
    return filingInfo

def convertPdfToExcelFile(inputPdfPath, inputFilename):
    with PdfReader(inputPdfPath) as pdf:
            for i, page in enumerate(pdf.pages):                
                
                # shortening the name to avoid Excel saying the name is too long and giving errors
                startIndex = inputFilename.find("Exhibit") # first, try to find 'Exhibit' in the filename
                if startIndex < 0: # if you don't find anything...
                    startIndex = inputFilename.find("Rates")  # then try to find 'Rates' in the filename
                    if startIndex < 0: # if still nothing...
                        startIndex = 0 # just use the whole filename (it'll be probably make Excel complain)
                excelFileName = f'{inputFilename[startIndex:-4]} Pg {i+1}.xlsx' # -4 cuts off '.pdf'
                
                # actually writing page to Excel file
                with pd.ExcelWriter(excelFileName) as excelWriter:
                    # replace() below should fix a few cases of pypdf seperating by comma on accident
                    text = page.extract_text().replace(" ,", ",")
                    if not text: continue # go to next page if page is empty
                    lines = text.split('\n') # Split text into lines
                    rows = []
                    for line in lines: rows.append(line.strip().split()) # convert lines of text into rows seperated by spaces
                    pd.DataFrame(rows).to_excel(excelWriter, index=False, header=False)

#--------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    # get tracking numbers from command-line arguments or else from user input
    trackingNums = []
    
    if (len(sys.argv) == 1): # if no arguments, get tracking numbers from user
        while True:
            trackingNum = input("Enter tracking number, or DONE: ")
            if trackingNum == "DONE": 
                break
            else: 
                trackingNums.append(trackingNum)
    else:
        # put each argument in list, excluding the script name
        for arg in sys.argv[1:]: 
            trackingNums.append(arg)
    
    # -----------------------------------------------------------    
    
    # make destination if it doesn't exist, then move into it
    if not os.path.exists(DESTINATION_PATH): os.makedirs(DESTINATION_PATH)
    os.chdir(DESTINATION_PATH)

    # make outer folder in downloads, with name of current date (if not exists)
    outerDir = str(time.strftime("%m-%d-%Y"))
    if not os.path.exists(outerDir): os.makedirs(outerDir)
    os.chdir(outerDir)
    
    for trackingNum in trackingNums:
        filingInfo = downloadBatch(os.path.join(DESTINATION_PATH, outerDir), trackingNum)
        if not filingInfo:
            print(f"{trackingNum} is an invalid tracking number. Make sure to try that one again.")
        else:
            batchPath = os.path.join(DESTINATION_PATH, outerDir, trackingNum)
            for file in os.listdir(batchPath):
                if file.endswith(".pdf"):
                    pdfPath = os.path.join(batchPath, file).replace("\\", "/")
                    convertPdfToExcelFile(pdfPath, file)

            # combine each page/excel file into one big excel file (1 per tracking number that is)
            os.chdir(os.path.join(DESTINATION_PATH, outerDir))
            combinedExcelPath = os.path.join(DESTINATION_PATH, outerDir, f'{trackingNum}.xlsx')
            excelWriter = pd.ExcelWriter(combinedExcelPath)
            for file in os.listdir(batchPath):
                if file.endswith(".xlsx"):
                    df = pd.read_excel(os.path.join(batchPath, file), header=None)
                    df.to_excel(excelWriter, sheet_name=file.replace(".xlsx", ""), header=False, index=False)
                    if not REMOVE_TRACKING_NUM_DIR: # no point in doing the following if the folder is deleted anyway
                        os.remove(os.path.join(batchPath, file)) # delete temporary Excel file, we don't need it no more
                    
            # save filing info to a sheet in file
            df = pd.DataFrame.from_dict(filingInfo, orient='index')
            # for label, value in filingInfo.items():
            #     df. writer.writerow([label, value])
            df.to_excel(excelWriter, sheet_name="Filing Info", header=False, index=True)
            
            excelWriter.close()
            
            if REMOVE_TRACKING_NUM_DIR:
                shutil.rmtree(batchPath) # deletes dir once Excel compilation is complete
        
    print("Process complete.")