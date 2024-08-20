# this is explicit for the invoices of the company "Minimax Mobile Services GmbH"
# the diferents with other invoices is that the number is places before the word "Rechnungsnummer"
# a solution is that, in the main app, if find a pdf with this company name, apply this specific patters.
# other solution is create a function for all the invoices that have the number before the word "Rechnungsnummer"

import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_file_path):
    text = ''
    
    # Try to extract text from the PDF using pdfplumber
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            # Extract text from the page
            page_text = page.extract_text()
            if page_text:
                text += page_text
    
    return text

def extract_invoice_number(text):
    # Print the extracted text for debugging
    print("Extracted Text:\n", text)
    
    # Define patterns to capture the invoice number just before 'Rechnungsnummer'
    patterns = [
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
        r'(\d{8,})\s*Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers right before 'Rechnungsnummer'
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
    ]
    
    for pattern in patterns:
        invoice_number_match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if invoice_number_match:
           
            # Extracted invoice number
            invoice_number = invoice_number_match.group(1).strip()
            return invoice_number
    
    # If no match is found, return None
    return None

def get_files_in_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                files.append(os.path.join(root, filename))
    return files

def extract_invoices_from_folder(folder_path):
    invoices = {}
    files = get_files_in_folder(folder_path)

    for file in files:
        text = extract_text_from_pdf(file)
        invoice_number = extract_invoice_number(text)
        if invoice_number:
            invoices[os.path.basename(file)] = invoice_number
            print(f'File: {os.path.basename(file)}, Invoice Number: {invoice_number}')
        else:
            print(f'File: {os.path.basename(file)} - No invoice number found')

    return invoices

if __name__ == "__main__":
    folder_path = 'companies/Minimax_Mobile_Services_GmbH/invoice'  # Specify the folder containing the PDFs
    invoices = extract_invoices_from_folder(folder_path)

    # Print the dictionary with filenames and invoice numbers
    print("Invoices: ", invoices)
