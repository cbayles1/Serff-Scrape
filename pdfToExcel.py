import pdfplumber
import pandas as pd
from config import *

def getBodyEnd(lines, bodyStart, bodyLength):
    bodyEnd = bodyStart + bodyLength
    # out of bounds checking
    if (bodyStart < 0): bodyStart = 0
    if (bodyStart >= len(lines)): bodyStart = len(lines) - 1
    if (bodyEnd < 0): bodyEnd = 0
    if (bodyEnd >= len(lines)): bodyEnd = len(lines) - 1    

def convertPdfToExcel(pdfPath, excelPath, headerLine, bodyStart, numRowsInBody):    
    # Read the PDF file
    with pdfplumber.open(pdfPath) as pdf:
        with pd.ExcelWriter(excelPath) as excelWriter:
            for page in pdf.pages:
                rows = []
                text = page.extract_text().replace(" ,", "") # replace function will fix it seperating by comma on accident, but will break any other uses of commas
                if text:
                    # Split text into lines
                    lines = text.split('\n')
                    
                    header = lines[headerLine].split() # header is not part of the body, but should have the desired length for the body
                    bodyEnd = getBodyEnd(lines, bodyStart, numRowsInBody)

                    # transform table body lines into rows array
                    rows = []
                    for line in lines[bodyStart:bodyEnd]:
                        rows.append(line.strip().split())
                    
                    # Ensure all rows have the same number of columns as the header, or less
                    for i, row in enumerate(rows):
                        if (len(row) > len(header)):
                            rows[i] = row[:len(header)]

                    # Convert rows to DataFrame to Excel, sheet_name is grabbing the table title from line index 3
                    pd.DataFrame(rows, columns=header).to_excel(excelWriter, index=False, sheet_name=lines[3])

                print(f"PDF text has been successfully extracted, converted to a table, and saved to Excel at {excelPath}.")

if __name__ == "__main__":
    #pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"
    pdf_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"

    #excel_path = "/08-09-2024/AETN-133858040/AERT.xlsx"
    excel_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/AERT.xlsx"
    
    convertPdfToExcel(pdf_path, excel_path, 6, 7, 35)