import pdfplumber
import pandas as pd
from config import *
import xml.etree.ElementTree as ET

def getBodyEnd(lines, bodyStart, bodyLength):
    bodyEnd = bodyStart + bodyLength
    # out of bounds checking
    if (bodyStart < 0): bodyStart = 0
    if (bodyStart >= len(lines)): bodyStart = len(lines) - 1
    if (bodyEnd < 0): bodyEnd = 0
    if (bodyEnd >= len(lines)): bodyEnd = len(lines) - 1    

def convertPdfLinesToExcelTableBody(lines, excelWriter, bodyStart, numColumns, numRows, sheetName): 
    # transform table body lines into rows array, table headers are not included in this function
    rows = []
    bodyEnd = getBodyEnd(lines, bodyStart, numRows)
    for line in lines[bodyStart:bodyEnd]:
        rows.append(line.strip().split())
    
    # Ensure all rows have the right amount of columns, or less
    for i, row in enumerate(rows):
        if (len(row) > numColumns):
            rows[i] = row[:numColumns]

    # Convert rows to DataFrame to Excel
    pd.DataFrame(rows).to_excel(excelWriter, index=False, header=False, sheet_name=sheetName)


def translatePageFormat(excelWriter, pageRoot, lines):
    for sheet in pageRoot:
        if sheet.tag != "sheet": raise Exception(f"Invalid XML format, only <sheet>'s are allowed as children of <page>")
        else:
            if 'titleLineNumber' in sheet.attrib:
                sheetTitle = lines[int(sheet.attrib['titleLineNumber'])].strip()
            if 'title' in sheet.attrib:
                sheetTitle = sheet.attrib['title'] # title attribute takes priority over titleLineNumber
            for childElement in sheet:
                match childElement.tag:
                    
                    case "titleSection":
                        print("Title section")
                        
                    case "tableHeader":
                        print("Table header")
                        
                    case "tableBody":
                        start = int(childElement.attrib['start'])
                        numColumns = int(childElement.attrib['numColumns'])
                        numLines = int(childElement.attrib['numLines'])
                        convertPdfLinesToExcelTableBody(lines, excelWriter, start, numColumns, numLines, sheetTitle)
                        
                    case "tableFooter":
                        print("Table footer")

def convertPdfToExcelFile(inputPdfPath, outputExcelPath, pdfFormatName):
    # the format that each page follows, as defined in the approprite xml file
    pdfPageFormatTree = ET.parse(os.path.join(PDF_FORMATS_PATH, f'{pdfFormatName}.xml')).getroot()
    if pdfPageFormatTree.tag != 'page': raise Exception(f"Invalid format in XML file {pdfFormatName}.xml, root must be <page>")
    
    with pdfplumber.open(inputPdfPath) as pdf:
        with pd.ExcelWriter(outputExcelPath) as excelWriter:
            for page in pdf.pages:
                # replace() below will fix pdfplumber seperating by comma on accident, but will break any other uses of commas
                text = page.extract_text().replace(" ,", "")
                if not text: continue # go to next page if page is empty
                lines = text.split('\n') # Split text into lines 
                translatePageFormat(excelWriter, pdfPageFormatTree, lines)

if __name__ == "__main__":
    pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"
    #pdf_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"

    excel_path = "/08-09-2024/AETN-133858040/AERT.xlsx"
    #excel_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/AERT.xlsx"
    
    convertPdfToExcelFile(pdf_path, excel_path, "rates")
