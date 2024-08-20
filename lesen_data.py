import PyPDF2
import os

def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Create a PdfReader object
        pdf_reader = PyPDF2.PdfReader(file)
        # Extract text from each page
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() or ''  # Handle cases where text might be None

    return text

def get_files_in_folder(folder_path):
    files = []
    # Iterate over all files and subdirectories in the folder
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):  # Check if the file is a PDF
                # Append the full file path to the list of files
                files.append(os.path.join(root, filename))
    return files

def extract_texts_from_folder(folder_path):
    file_texts = {}
    files = get_files_in_folder(folder_path)

    for file in files:
        text = extract_text_from_pdf(file)
        file_texts[os.path.basename(file)] = text

    return file_texts

if __name__ == "__main__":
    folder_path = 'invoices'  # Specify the folder containing the PDFs
    file_texts = extract_texts_from_folder(folder_path)

    # Print the text extracted from each file
    for file_name, text in file_texts.items():
        print(f"File: {file_name}")
        print("Extracted Text:")
        print(text)
        print("\n" + "="*50 + "\n")  # Separator between files
