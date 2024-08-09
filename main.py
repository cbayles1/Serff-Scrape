import os, shutil, time, datetime, csv, sys
from config import *
from scraper import *

def downloadBatch(parentPath, trackingNum):
    
    batchPath = os.path.join(parentPath, trackingNum)
    # make inner folder with name of tracking number (if not exists)
    if not os.path.exists(batchPath): os.makedirs(batchPath)
    os.chdir(batchPath)

    print(f"Downloading batch {trackingNum}...")
    # download each batch, then move into corresponding folder
    filingInfo = runScraper(trackingNum, DRIVER_PATH)
    for file in os.listdir(DOWNLOADS_PATH):
        src = os.path.join(DOWNLOADS_PATH, file).replace("\\", "/")
        dest = os.path.join(batchPath, file).replace("\\", "/")
        
        # If file was created a minute or less ago, it is moved from the DOWNLOADS_PATH to the DESTINATION_PATH
        creation = datetime.datetime.fromtimestamp(os.stat(src).st_ctime)
        now = datetime.datetime.now()
        if creation >= now - datetime.timedelta(minutes=1):
            shutil.move(src, dest) # move file
    
    print(f"Downloading bfiling info for {trackingNum}...")
    # save filing info as .csv
    csvPath = os.path.join(batchPath, 'filing_info.csv')
    with open(csvPath, 'w', newline='') as f:
        writer = csv.writer(f)
        for label, value in filingInfo.items():
            writer.writerow([label[:-1], value]) # [:-1] removes the colon

if __name__ == "__main__": 
    
    # get tracking numbers from command-line arguments
    trackingNums = []
    for arg in sys.argv[1:]: # put each argument in list, excluding the script name
        trackingNums.append(arg)
    
    # make destination if it doesn't exist, then move into it
    if not os.path.exists(DESTINATION_PATH): os.makedirs(DESTINATION_PATH)
    os.chdir(DESTINATION_PATH)

    # make outer folder in downloads, with name of current date (if not exists)
    outerDir = str(time.strftime("%m-%d-%Y"))
    if not os.path.exists(outerDir): os.makedirs(outerDir)
    os.chdir(outerDir)
    
    for trackingNum in trackingNums:
        downloadBatch(os.path.join(DESTINATION_PATH, outerDir), trackingNum)