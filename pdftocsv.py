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
pdf_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/2024 ACC IA MIPPA Rates.pdf"

# Initialize a list to hold rows of data
rows = []

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            # Split text into lines
            lines = text.split('\n')
            
            # Print lines to debug
            print("Extracted lines:")
            for line in lines:
                print(line)
            
            # Handle multi-line rows and extract header
            header = lines[0].split()  # Adjust based on actual delimiter
            print("Header:", header)
            
            for line in lines[1:]:
                # If lines are split inconsistently, try joining parts
                if len(line.split()) < len(header):
                    # Handle cases where data might be split across lines
                    # Join with the previous line if it appears to be split
                    if rows and len(rows[-1]) < len(header):
                        rows[-1].append(line.strip())
                    else:
                        # Otherwise, just add a new row
                        columns = line.split()  # Adjust based on actual delimiter
                        rows.append(columns)
                else:
                    columns = line.split()  # Adjust based on actual delimiter
                    rows.append(columns)

# Debug: Print first few rows and header
print("Rows preview:", rows[:10])

# Ensure all rows have the same number of columns as the header
num_columns = len(header)
rows = [row for row in rows if len(row) == num_columns]

# Debug: Print rows count and a few rows
print(f"Number of rows: {len(rows)}")
print("Rows preview after cleaning:", rows[:10])

# Create DataFrame from rows
df = pd.DataFrame(rows, columns=header)

# Define the Excel file path
excel_path = "A:/SERFF Filings/08-09-2024/AETN-133858040/AERT.xlsx"

# Save DataFrame to Excel
df.to_excel(excel_path, index=False)

print(f"PDF text has been successfully extracted, converted to a table, and saved to Excel at {excel_path}.")

