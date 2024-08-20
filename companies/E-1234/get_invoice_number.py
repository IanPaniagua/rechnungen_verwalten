import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_file_path):
    text = ''
    
    # Extract text from each page of the PDF using pdfplumber
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            # Extract text from the page
            page_text = page.extract_text()
            if page_text:
                text += page_text
    
    return text

def extract_invoice_number(text):
    # Print the extracted text for debugging purposes
    print("Extracted Text:\n", text)
    
    # Define a pattern to find the invoice number after the phrase "Rechnung Nr."
    pattern = r'(?:Rechnung\s*Nr\.?|Rechnungs-Nr\.?|Rechnungsnummer)[\s:]*[-\s]*([\w\d-]+)'  # Matches "Rechnung Nr." followed by the invoice number in the format 24-07210
    
    # Attempt to find a match using the defined pattern
    match = re.search(pattern, text)
    if match:
        # Return the captured invoice number, ensuring any leading/trailing spaces are removed
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
    invoices = {}
    files = get_files_in_folder(folder_path)

    for file in files:
        # Extract text from each PDF file
        text = extract_text_from_pdf(file)
        # Attempt to extract the invoice number from the extracted text
        invoice_number = extract_invoice_number(text)
        if invoice_number:
            # Store the invoice number in a dictionary with the filename as the key
            invoices[os.path.basename(file)] = invoice_number
            print(f'File: {os.path.basename(file)}, Invoice Number: {invoice_number}')
        else:
            print(f'File: {os.path.basename(file)} - No invoice number found')

    return invoices

if __name__ == "__main__":
    folder_path = 'companies/E-1234/invoice'  # Specify the folder containing the PDFs
    invoices = extract_invoices_from_folder(folder_path)

    # Print the dictionary with filenames and invoice numbers
    print("Invoices: ", invoices)
