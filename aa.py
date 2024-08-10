import pdfplumber
import pandas as pd

def parseTableBody(header, body): # header is not included in body
    rows = []
    temp_row = []

    for line in body:
        # If lines are split inconsistently, try joining parts
        line = line.strip()
        if len(line.split()) < len(header):
            # If the current line is shorter than the header, assume it should be joined with the previous line
            if temp_row:
                temp_row.append(line)
            else:
                temp_row = line.split()
        else:
            # If there is a collected temporary row, add it to rows
            if temp_row:
                rows.append(temp_row)
                temp_row = []
            rows.append(line.split())
    
    # If there's any remaining temporary row, add it to rows
    if temp_row:
        rows.append(temp_row)

    return rows

def convertPdfToExcel(pdfPath, excelPath, headerLine, bodyStart, bodyEnd):
    rows = []
    
    # Read the PDF file
    with pdfplumber.open(pdfPath) as pdf:
        for page in pdf.pages:
            text = page.extract_text().replace(" ,", ",")  # replace function will fix it separating by comma on accident
            if text:
                # Split text into lines
                lines = text.split('\n')
                
                header = lines[headerLine].split()
                
                rows = parseTableBody(header, lines[bodyStart:bodyEnd])
                
                # Ensure all rows have the same number of columns as the header
                rows = [row for row in rows if len(row) == len(header)]

    # Create DataFrame from rows
    df = pd.DataFrame(rows, columns=header)

    # Save DataFrame to Excel
    df.to_excel(excelPath, index=False)

    print(f"PDF text has been successfully extracted, converted to a table, and saved to Excel at {excelPath}.")

# Paths to files
pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"
excel_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/New Microsoft Excel Worksheet.xlsx"

convertPdfToExcel(pdf_path, excel_path, 6, 7, 42)