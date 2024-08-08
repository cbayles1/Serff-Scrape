from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# -----------------------------HELPER FUNCTIONS

def getElementsOnceLoaded(identifierType, identifierContent, multiple=True, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((identifierType, identifierContent))
    )
    if multiple:
        return driver.find_elements(identifierType, identifierContent)
    else: 
        return driver.find_element(identifierType, identifierContent)
    
def getElementOnceLoaded(identifierType, identifierContent, timeout=5):
    return getElementsOnceLoaded(identifierType, identifierContent, False, timeout)
    
# ----------------------------------------------------------------------------------

# page to keep session active

driver.get("https://filingaccess.serff.com/sfa/home/IA")
driver.maximize_window()

beginBtn = getElementOnceLoaded(By.CLASS_NAME, "btn-success")
beginBtn.click()

# ----------------------------------------------------------------------------------

# user agreement page

btns = getElementsOnceLoaded(By.CLASS_NAME, "ui-button-text-only") # Accept and Decline buttons
acceptBtn = btns[0] # First button should be the accept button

acceptBtn.click()

# ----------------------------------------------------------------------------------

# search form

trackingNumber = "AETN-133858040"

inputBox = getElementOnceLoaded(By.ID, "simpleSearch:serffTrackingNumber")

inputBox.clear()
inputBox.send_keys(trackingNumber)
inputBox.send_keys(Keys.ENTER)

# ----------------------------------------------------------------------------------

# search results

btn = getElementOnceLoaded(By.CLASS_NAME, "ui-datatable-even")
btn.click() # Company button within search results


# ----------------------------------------------------------------------------------

# grab filing information

# filingInfo = {} # dictionary to hold each pair of info
# filingSummaries = getElementsOnceLoaded(By.CSS_SELECTOR, 'div.col-lg-6')
# filingInfoElement = filingSummaries[0]
# print(filingInfoElement.get_attribute('class'))

# ----------------------------------------------------------------------------------

# grab files

blacklistedAttachmentIds = [  # the pattern seems to be j_idt195:INDEX_OF_SECTION:j_idt200:INDEX_OF_FILE_WITHIN_SECTION:downloadAttachment_ (starting at 0, not 1)
    "summaryForm:j_idt195:0:j_idt200:0:downloadAttachment_",
    "summaryForm:j_idt195:2:j_idt200:1:downloadAttachment_",
    "summaryForm:j_idt195:4:j_idt200:0:downloadAttachment_"
]

files = getElementsOnceLoaded(By.CLASS_NAME, "ui-commandlink") # all attachments
for attachment in files:
    if not attachment.get_attribute('id') in blacklistedAttachmentIds: # don't download files in blacklist
        attachment.click() # download each file

# ----------------------------------------------------------------------------------

driver.quit()