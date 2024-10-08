from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import *

def runScraper(trackingNumber, driverPath, state):
    
    service = Service(executable_path=driverPath)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument('user-agent={0}'.format('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'))
    driver = webdriver.Chrome(service=service, options=options)
    
    # ----------------------------------------------------------------------------------
    
    # page to keep session active

    driver.get(f"https://filingaccess.serff.com/sfa/home/{state}")
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
    try: inputBox.send_keys(trackingNumber)
    except: raise Exception("Invalid tracking number.")
    inputBox.send_keys(Keys.ENTER)

    # ----------------------------------------------------------------------------------

    # search results

    btn = getElementOnceLoaded(driver, By.CLASS_NAME, "ui-datatable-even")
    btn.click() # Company button within search results

    # ----------------------------------------------------------------------------------

    # grab filing information, breaks easily if NAIC changes the page's layout
   
    filingInfo = {} # dictionary to hold all the info, by row, will be saved as a .csv at the very end
   
    for i in range(7): # there's currently 7 rows of info under Filing Information
        pathToRow = f"//div[@id='bodyContentWrapper']/div[1]/div[1]/div[1]/div[1]/div[{i+1}]/" # very fragile to page structure
        rowLabel = getElementOnceLoaded(driver, By.XPATH, pathToRow + "label[1]").text
        rowValue = getElementOnceLoaded(driver, By.XPATH, pathToRow + "div[1]").text
        filingInfo[rowLabel[:-1]] = rowValue # [:-1] removes the colon
    
    # ----------------------------------------------------------------------------------

    # grab files

    files = getElementsOnceLoaded(driver, By.CLASS_NAME, "ui-commandlink") # all attachments
    for attachment in files:
        
        # if any blacklisted phrases are found in the title of any attachment (class "ui-commandlink"), it will not be downloaded
        if not any((phrase in attachment.text) for phrase in blacklistedAttachments):
            attachment.click() # download each file

    # ----------------------------------------------------------------------------------

    time.sleep(TEMP_FILE_TIMEOUT)
    driver.quit()
    
    return filingInfo
    
    # ----------------------------------------------------------------------------------

def getElementsOnceLoaded(driver, identifierType, identifierContent, multiple=True, timeout=5):
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.visibility_of_element_located((identifierType, identifierContent))
    )
    if multiple:
        return driver.find_elements(identifierType, identifierContent)
    else: 
        return driver.find_element(identifierType, identifierContent)
    
def getElementOnceLoaded(driver, identifierType, identifierContent, timeout=5):
    return getElementsOnceLoaded(driver, identifierType, identifierContent, False, timeout)