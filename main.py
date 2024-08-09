import os, shutil, time, datetime
from config import *
from scraper import *

# make destination if it doesn't exist, then move into it
if not os.path.exists(DESTINATION_PATH): os.makedirs(DESTINATION_PATH)
os.chdir(DESTINATION_PATH)

# make outer folder in downloads, with name of current date (if not exists)
outerDir = str(time.strftime("%m-%d-%Y"))
if not os.path.exists(outerDir): os.makedirs(outerDir)
os.chdir(outerDir)

while True:
    # get tracking number from user
    trackingNum = input("Enter tracking number, or QUIT: ")
    if trackingNum == "QUIT": break

    # make inner folder with name of tracking number (if not exists)
    if not os.path.exists(trackingNum): os.makedirs(trackingNum)
    os.chdir(trackingNum)

    # download each batch, then move into corresponding folder
    filingInfo = runScraper(trackingNum, DRIVER_PATH)
    for file in os.listdir(DOWNLOADS_PATH):
        src = os.path.join(DOWNLOADS_PATH, file).replace("\\", "/")
        dest = os.path.join(DESTINATION_PATH, outerDir, trackingNum, file).replace("\\", "/")
            
        # If file was created a minute or less ago, it is moved from the DOWNLOADS_PATH to the DESTINATION_PATH
        creation = datetime.datetime.fromtimestamp(os.stat(src).st_ctime)
        now = datetime.datetime.now()
        if creation >= now - datetime.timedelta(minutes=1):
            shutil.move(src, dest)
    
    # save filing info as .csv
    csvPath = os.path.join(DESTINATION_PATH, outerDir, trackingNum, 'filing_info.csv')
    with open(csvPath, 'w', newline='') as f:
        writer = csv.writer(f)
        for label, value in filingInfo.items():
            writer.writerow([label[:-1], value]) # [:-1] removes the colon
    
    # return to parent directory
    os.chdir('..')