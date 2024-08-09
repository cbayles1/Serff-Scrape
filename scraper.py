from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import *

def runScraper(trackingNumber, driverPath):
    
    service = Service(executable_path=driverPath)
    driver = webdriver.Chrome(service=service)
    
    # ----------------------------------------------------------------------------------
    
    # page to keep session active

    driver.get("https://filingaccess.serff.com/sfa/home/IA")
    driver.maximize_window()

    beginBtn = getElementOnceLoaded(driver, By.CLASS_NAME, "btn-success")
    beginBtn.click()

    # ----------------------------------------------------------------------------------

    # user agreement page

    btns = getElementsOnceLoaded(driver, By.CLASS_NAME, "ui-button-text-only") # Accept and Decline buttons
    acceptBtn = btns[0] # First button should be the accept button

    acceptBtn.click()

    # ----------------------------------------------------------------------------------

    # search form

    inputBox = getElementOnceLoaded(driver, By.ID, "simpleSearch:serffTrackingNumber")

    inputBox.clear()
    inputBox.send_keys(trackingNumber)
    inputBox.send_keys(Keys.ENTER)

    # ----------------------------------------------------------------------------------

    # search results

    btn = getElementOnceLoaded(driver, By.CLASS_NAME, "ui-datatable-even")
    btn.click() # Company button within search results


    # ----------------------------------------------------------------------------------

    # grab filing information

    # filingInfo = {} # dictionary to hold each pair of info
    # filingSummaries = getElementsOnceLoaded(driver, By.CSS_SELECTOR, 'div.col-lg-6')
    # filingInfoElement = filingSummaries[0]
    # print(filingInfoElement.get_attribute('class'))

    # ----------------------------------------------------------------------------------

    # grab files

    files = getElementsOnceLoaded(driver, By.CLASS_NAME, "ui-commandlink") # all attachments
    for attachment in files:
        # if not attachment.get_attribute('id') in blacklistedAttachmentIds: # don't download files in blacklist
        #     attachment.click() # download each file
        attachment.click() # download each file

    # ----------------------------------------------------------------------------------

    time.sleep(10)
    driver.quit()
    
    # ----------------------------------------------------------------------------------
    
def getElementsOnceLoaded(driver, identifierType, identifierContent, multiple=True, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((identifierType, identifierContent))
    )
    if multiple:
        return driver.find_elements(identifierType, identifierContent)
    else: 
        return driver.find_element(identifierType, identifierContent)
    
def getElementOnceLoaded(driver, identifierType, identifierContent, timeout=5):
    return getElementsOnceLoaded(driver, identifierType, identifierContent, False, timeout)

if __name__ == "__main__":
    runScraper("AETN-133858040", "chromedriver.exe")