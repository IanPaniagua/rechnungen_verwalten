import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from io import BytesIO
import os
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_file_path):
    text = ''
    
    # Open the PDF file
    try:
        doc = fitz.open(pdf_file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()  # Render page to an image
            img = Image.open(BytesIO(pix.tobytes()))  # Convert to PIL Image
            # Use pytesseract to extract text from the image
            text += pytesseract.image_to_string(img, lang='eng+deu', config='--psm 6')
    except Exception as e:
        print(f"Error using OCR on {pdf_file_path}: {e}")
    
    return text

def extract_invoice_number(text):
    # Print the extracted text for debugging
    print("Extracted Text:\n", text)
    
    # Define patterns to capture various invoice number formats
    patterns = [
        r'Rechnungsnr\.\s*:\s*(RE\d+)',  # Example pattern for MAXEDV
        r'Rechnung\s+(\d{4}/\d{4})',  # Example pattern for Lindemann Elektrotechnik
        r'(?:Rechnung\s*Nr\.?|Rechnungs-Nr\.?|Rechnungsnummer)[\s:]*[-\s]*([\w\d-]+)',  # Example pattern for E-1234
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer\s*[:\s]*',  # Example pattern for 8 or more digits before Rechnungsnummer
        r'(\d{8,})\s*Rechnungsnummer\s*[:\s]*',  # Example pattern for 8 or more digits right before Rechnungsnummer
        r'(\d{8,})\s*[\s\S]*?Rechnungsnummer',  # Example pattern for 8 or more digits before Rechnungsnummer
    ]
    
    # Check each pattern from the previous formats
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

def extract_invoices_from_folder(folder_path):
    invoices = []
    files = get_files_in_folder(folder_path)

    for file in files:
        print(f"Processing file: {file}")
        text = extract_text_from_pdf(file)
        if not text:
            print(f"No text extracted from file: {file}")
        invoice_number = extract_invoice_number(text)
        if invoice_number:
            invoices.append((os.path.basename(file), invoice_number))
        else:
            invoices.append((os.path.basename(file), 'No invoice number found'))

    return invoices

def display_invoices(invoices, filename_width=20):
    print(f"{'Filename':<{filename_width}} {'Rechnungsnummer':<25}")
    print("=" * (filename_width + 25))
    for filename, invoice_number in invoices:
        # Truncate filenames if they are too long
        if len(filename) > filename_width:
            filename = filename[:filename_width - 3] + "..."
        print(f"{filename:<{filename_width}} {invoice_number:<25}")

if __name__ == "__main__":
    folder_path = 'companies/Glas_Land_GmbH/invoice'  # Specify the folder containing the PDFs
    if not os.path.exists(folder_path):
        print(f"Folder path '{folder_path}' does not exist.")
    else:
        invoices = extract_invoices_from_folder(folder_path)
        # Display the results
        display_invoices(invoices)
