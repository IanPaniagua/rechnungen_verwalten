from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import os
import re

def extract_text_from_pdf(pdf_file_path):
    text = ''
    
    # Try to extract text using pdfplumber first
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF with pdfplumber: {e}")
    
    # If text extraction failed or if the document is scanned, use OCR
    if not text.strip():
        print(f"Using OCR for file: {pdf_file_path}")
        # Convert PDF pages to images
        try:
            images = convert_from_path(pdf_file_path)
            for image in images:
                # Use pytesseract to extract text from each image in both English and German
                text += pytesseract.image_to_string(image, lang='eng+deu', config='--psm 6')
        except Exception as e:
            print(f"Error using OCR: {e}")
    
    return text

def get_files_in_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                files.append(os.path.join(root, filename))
    return files

def extract_invoices_from_folder(folder_path):
    invoices = []
    files = get_files_in_folder(folder_path)

    for file in files:
        text = extract_text_from_pdf(file)
        invoice_number = extract_invoice_number(text)
        if invoice_number:
            invoices.append((os.path.basename(file), invoice_number))
        else:
            invoices.append((os.path.basename(file), 'No invoice number found'))

    return invoices

def extract_invoice_number(text):
    # Define patterns to capture various invoice number formats
    patterns = [
        r'Rechnungsnr\.\s*:\s*(RE\d+)', # (MAXEDV)
        r'Rechnung\s+(\d{4}/\d{4})',  # Pattern for "Rechnung" followed by a format like 2024/0141 (Lindemann Elektrotechnik)
        r'(?:Rechnung\s*Nr\.?|Rechnungs-Nr\.?|Rechnungsnummer)[\s:]*[-\s]*([\w\d-]+)',  # Pattern for other formats (E-1234)
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
        r'(\d{8,})\s*Rechnungsnummer\s*[:\s]*',  # Captures 8 or more digit numbers right before 'Rechnungsnummer'
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer',  # Captures 8 or more digit numbers before 'Rechnungsnummer'
    ]
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Check for invoice number formats where the number is on the next line
    for i, line in enumerate(lines):
        if 'Rechnungs-Nr.' in line:
            next_line = lines[i + 1] if i + 1 < len(lines) else ''
            pattern = r'\b(\d{6,})\b'  # Pattern for 6 or more digits
            match = re.search(pattern, next_line)
            if match:
                return match.group(1).strip()
    
    # Check each pattern from the previous formats
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    # If no match is found, return None
    return None

def display_invoices(invoices, filename_width=20):
    print(f"{'Filename':<{filename_width}} {'Rechnungsnummer':<25}")
    print("=" * (filename_width + 25))
    for filename, invoice_number in invoices:
        # Truncate filenames if they are too long
        if len(filename) > filename_width:
            filename = filename[:filename_width - 3] + "..."  # Truncate and add ellipsis
        print(f"{filename:<{filename_width}} {invoice_number:<25}")

if __name__ == "__main__":
    # Specify the folder containing the PDFs
    folder_path = r'C:\Users\Teilnehmer\OneDrive - BBQ - Baumann Bildung und Qualifizierung GmbH\Dokumente\GitHub\rechnungen_verwalten\re_'
    
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Folder path '{folder_path}' does not exist.")
        exit()
    
    invoices = extract_invoices_from_folder(folder_path)

    # Display the results
    display_invoices(invoices)
