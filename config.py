DOWNLOADS_PATH = "C:/Users/charl/Downloads"
DESTINATION_PATH = "A:/SERFF Filings"
DRIVER_PATH = "A:/serffScrape/serffScrape/chromedriver.exe"
TEMP_FILE_TIMEOUT = 5

# if any of these phrases are found in the title of any attachment (class "ui-commandlink"), it will not be downloaded
blacklistedAttachments = [
    ".xlsx",
    "Actuarial Certification"
]
