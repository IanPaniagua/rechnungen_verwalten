import pdfplumber
import re
import os
import shutil

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
    
    # Define patterns to capture various invoice number formats
    patterns = [
        r'Rechnungsnr\.\s*:\s*(RE\d+)', # (MAXEDV)
        r'Rechnung\s+(\d{4}/\d{4})',  # Pattern for "Rechnung" followed by a format like 2024/0141 (Lindemann Elektrotechnik)
        r'(?:Rechnung\s*Nr\.?|Rechnungs-Nr\.?|Rechnungsnummer)[\s:]*[-\s]*([\w\d-]+)',  # Pattern for other formats (E-1234)
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
        r'(\d{8,})\s*Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers right before 'Rechnungsnummer'
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
    ]
    
    # Check each pattern
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    # If no match is found, return None
    return None

def get_files_in_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                files.append(os.path.join(root, filename))
    return files

def move_file_to_folder(file_path, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))

def extract_invoices_from_folder(folder_path, target_folder):
    invoices = {}
    files = get_files_in_folder(folder_path)

    for file in files:
        text = extract_text_from_pdf(file)
        invoice_number = extract_invoice_number(text)
        if invoice_number:
            invoices[os.path.basename(file)] = invoice_number
            print(f'File: {os.path.basename(file)}, Invoice Number: {invoice_number}')
            # Move the file to the target folder
            move_file_to_folder(file, target_folder)
        else:
            print(f'File: {os.path.basename(file)} - No invoice number found')

    return invoices

if __name__ == "__main__":
    folder_path = 're_'  # Specify the folder containing the PDFs
    target_folder = 're_erledigt'  # Specify the target folder for processed files
    invoices = extract_invoices_from_folder(folder_path, target_folder)

    # Print the dictionary with filenames and invoice numbers
    print("Invoices: ", invoices)
