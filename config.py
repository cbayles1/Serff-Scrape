from dotenv import load_dotenv
import os

load_dotenv() # Looks for a .env file in the current directory and opens it

# grabs each from the .env file, which is not on the GitHub and is made by each developer
DOWNLOADS_PATH = os.getenv('DOWNLOADS_PATH')
DESTINATION_PATH = os.getenv('DESTINATION_PATH')
DRIVER_PATH = os.getenv('DRIVER_PATH')
TEMP_FILE_TIMEOUT = 10
REMOVE_TRACKING_NUM_DIR = True

# if any of these phrases are found in the title of any attachment (class "ui-commandlink"), it will not be downloaded
blacklistedAttachments = [
    "Certificate of Compliance",
    "Actuarial Certification",
    "Actuarial Memo",
    "Exhibit 1.pdf",
    "Actuarial Memo Revised",
    "Exhibit 1 Revised.pdf"
]