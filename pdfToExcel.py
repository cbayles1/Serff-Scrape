import pdfplumber
import pandas as pd

def parseTableBody(header, body): # header is not included in body
    rows = []
    for line in body:
        # # If lines are split inconsistently, try joining parts
        # if len(line.split()) < len(header):
            
        #     # Handle cases where data might be split across lines
        #     # Join with the previous line if it appears to be split
        #     if rows and len(rows[-1]) < len(header):
        #         rows[-1].append(line.strip())
        #     else:
        #         # Otherwise, just add a new row
        #         columns = line.split()
        #         rows.append(columns)
        # else:
        #     columns = line.split()
        #     rows.append(columns)
        rows.append(line.strip().split())
            
    return rows

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
                    
                    header = lines[headerLine].split()
                    
                    bodyEnd = bodyStart + numRowsInBody
                    # out of bounds checking
                    if (bodyStart < 0): bodyStart = 0
                    if (bodyStart >= len(lines)): bodyStart = len(lines) - 1
                    if (bodyEnd < 0): bodyEnd = 0
                    if (bodyEnd >= len(lines)): bodyEnd = len(lines) - 1
                    
                    rows = parseTableBody(header, lines[bodyStart:bodyEnd])
                    
                    # Ensure all rows have the same number of columns as the header, or less
                    #rows = [row for row in rows if len(row) <= len(header)]
                    for i, row in enumerate(rows):
                        if (len(row) > len(header)):
                            rows[i] = row[:len(header)]

                    # Create DataFrame from rows
                    df = pd.DataFrame(rows, columns=header)

                    # Save DataFrame to Excel, sheet_name is grabbing the table title from line index 3
                    df.to_excel(excelWriter, index=False, sheet_name=lines[3])

                print(f"PDF text has been successfully extracted, converted to a table, and saved to Excel at {excelPath}.")

#pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"
pdf_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"

#excel_path = "/08-09-2024/AETN-133858040/AERT.xlsx"
excel_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/AERT.xlsx"

convertPdfToExcel(pdf_path, excel_path, 6, 7, 35)