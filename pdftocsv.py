#pip install openpyxl
#pip install pandas
#pip install pdfplumber
#import tabula

#inp = (r"A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf")
#oup = (r"test.csv")

#df = tabula.read_pdf(input_path=inp, pages="all")
#tabula.convert_into(input_path=inp, output_path=oup, output_format="csv", pages="all", stream=True)

#import re
#from pdfminer.high_level import extract_pages, extract_text

#for page_layout in extract_pages("A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"):
#    for element in page_layout:
#        print(element)

#text = extract_text("A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf")

import pdfplumber
import pandas as pd

# Define the PDF file path
#pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"
pdf_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"

# Initialize a list to hold rows of data
rows = []

def parseTableBody(header, body): # header is not included in body
    rows = []
    for line in body:
        
        # If lines are split inconsistently, try joining parts
        if len(line.split()) < len(header):
            
            # Handle cases where data might be split across lines
            # Join with the previous line if it appears to be split
            if rows and len(rows[-1]) < len(header):
                rows[-1].append(line.strip())
            else:
                # Otherwise, just add a new row
                columns = line.split()
                rows.append(columns)
        else:
            columns = line.split()
            rows.append(columns)
            
    return rows

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text().replace(" ,", ",") # replace function will fix it seperating by comma on accident, but will break any other uses of commas
        if text:
            # Split text into lines
            lines = text.split('\n')
            
            header = lines[6].split()
            rows = parseTableBody(header, lines[7:])
            
            # Ensure all rows have the same number of columns as the header, or less
            num_columns = len(header)
            rows = [row for row in rows if len(row) <= num_columns]

# Create DataFrame from rows
df = pd.DataFrame(rows, columns=header)

# Define the Excel file path
#excel_path = "/08-09-2024/AETN-133858040/AERT.xlsx"
excel_path = "H:/clbay/CodeProjects/serffScrape/output/08-09-2024/AETN-133858040/AERT.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"PDF text has been successfully extracted, converted to a table, and saved to Excel at {excel_path}.")

