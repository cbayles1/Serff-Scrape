import os, shutil, time
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
    runScraper(trackingNum, DRIVER_PATH)
    for file in os.listdir(DOWNLOADS_PATH):
        src = os.path.join(DOWNLOADS_PATH, file)
        dest = os.path.join(DESTINATION_PATH, outerDir, trackingNum, file)
        shutil.move(src, dest)
    
    # return to parent directory
    os.chdir('..')