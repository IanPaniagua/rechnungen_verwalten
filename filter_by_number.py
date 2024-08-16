import PyPDF2
import os
import re
import shutil

def extract_invoice_info(pdf_file_path):
    """Extract information from an invoice PDF file."""
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        # Regular expressions for different sections of the invoice
        invoice_number_pattern = r'Invoice Number\s+(\S+)'  # Captures the invoice number
        bill_to_pattern = r'To:\s+([\s\S]+?)\nHrs/Qty'  # Captures the "Bill To" section up to "Hrs/Qty"
        items_pattern = r'Hrs/Qty\s+Service\s+Rate/Price\s+Adjust\s+([\s\S]+?)\nSub Total'  # Captures the items list
        notes_terms_pattern = r'(?<=Invoice)([\s\S]+?)Page 1/1'  # Captures the terms section near "Invoice"
        discount_tax_pattern = r'(\d+\.\d+%)'  # Captures discount or tax percentages

        # Extract information using regular expressions
        invoice_number_match = re.search(invoice_number_pattern, text)
        bill_to_match = re.search(bill_to_pattern, text)
        items_match = re.search(items_pattern, text)
        notes_terms_match = re.search(notes_terms_pattern, text)
        discount_tax_matches = re.findall(discount_tax_pattern, text)

        # Extracted information
        invoice_number = invoice_number_match.group(1) if invoice_number_match else None
        bill_to = bill_to_match.group(1).strip() if bill_to_match else None
        items = items_match.group(1).strip() if items_match else None
        notes_terms = notes_terms_match.group(1).strip() if notes_terms_match else None
        discount_percentage = discount_tax_matches[0] if len(discount_tax_matches) > 0 else None
        tax_percentage = discount_tax_matches[1] if len(discount_tax_matches) > 1 else None

    return invoice_number, bill_to, items, notes_terms, discount_percentage, tax_percentage

def get_files_in_folder(folder_path):
    """Get a list of all files in the specified folder."""
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def process_invoices(folder_path, target_invoice_number, processed_folder):
    """Process invoices in the folder, check for specific invoice number, and move file accordingly."""
    files = get_files_in_folder(folder_path)
    os.makedirs(processed_folder, exist_ok=True)

    for file in files:
        print("Processing File: ", file)
        invoice_number, bill_to, items, notes_terms, discount_percentage, tax_percentage = extract_invoice_info(file)

        # Print extracted information
        print("Invoice Number: ", invoice_number)
        print("Bill To: ", bill_to)
        print("Items: ", items)
        print("Notes and Terms: ", notes_terms)
        print("Discount Percentage: ", discount_percentage)
        print("Tax Percentage: ", tax_percentage)

        # Check if the invoice number matches the target number
        if invoice_number == target_invoice_number:
            # Move the file to the processed folder
            new_file_path = os.path.join(processed_folder, os.path.basename(file))
            shutil.move(file, new_file_path)
            print(f"File with Invoice Number {invoice_number} moved to {processed_folder}")
        else:
            print(f"File with Invoice Number {invoice_number} did not match the target number.")

if __name__ == "__main__":
    folder_path = 'invoices'
    target_invoice_number = 'INV-3337'  # Replace with the specific invoice number you're looking for
    processed_folder = 'processed_invoices'

    process_invoices(folder_path, target_invoice_number, processed_folder)
