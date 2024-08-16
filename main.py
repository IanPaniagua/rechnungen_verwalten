import PyPDF2
import os
import re

def extract_invoice_info(pdf_file_path):
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Create a PdfReader object
        pdf_reader = PyPDF2.PdfReader(file)
        # Extract text from each page
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

        # Print results
        # if invoice_number:
        #     print(f"Invoice Number: {invoice_number}")
        # else:
        #     print("Invoice Number not found.")

        # if bill_to:
        #     print(f"Bill To: {bill_to}")
        # else:
        #     print("Bill To not found.")

        # if items:
        #     print(f"Items: {items}")
        # else:
        #     print("Items not found.")

        # if discount_percentage:
        #     print(f"Discount Percentage: {discount_percentage}")
        # else:
        #     print("Discount Percentage not found.")

        # if tax_percentage:
        #     print(f"Tax Percentage: {tax_percentage}")
        # else:
        #     print("Tax Percentage not found.")

        # if notes_terms:
        #     print(f"Notes and Terms: {notes_terms}")
        # else:
        #     print("Notes and Terms not found.")

    return invoice_number, bill_to, items, notes_terms, discount_percentage, tax_percentage

def get_files_in_folder(folder_path):
    files = []
    # Iterate over all files and subdirectories in the folder
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            #Append the full file path to the list of files
            files.append(os.path.join(root, filename))
        return files
    
if __name__ == "__main__":
    folder_path = 'invoices'
    files  = get_files_in_folder(folder_path)

    for file in files:
        print("File: ", file)
        invoice_number, bill_to, items, notes_terms, discount_percentage, tax_percentage = extract_invoice_info(file)

        # Print extracted information
        print("Invoice Number: ", invoice_number)
        print("bill_to: ", bill_to)
        print("items: ", items)
        print("notes_terms: ", notes_terms)
        print("discount_percentage: ", discount_percentage)
        print("tax_percentage: ", tax_percentage)
     
      
        # Move the processed file to a different folder
        processed_folder = 'processed_invoices'
        os.makedirs(processed_folder, exist_ok=True)
        new_file_path = os.path.join(processed_folder, os.path.basename(file))
        os.rename(file, new_file_path)