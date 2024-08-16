# Invoice Processor

## Overview

main.py : This project processes invoice PDFs by extracting key information and moving the files based on specific criteria. It uses Python for PDF parsing and regular expressions to locate and extract details such as invoice numbers, bill-to addresses, item descriptions, notes and terms, and percentages for discounts and taxes.

filter_by_number.py: allows you to filter the pdf by a specific number.
## Features

- **Extract Invoice Information**: Extracts invoice number, bill-to address, item details, notes and terms, and discount/tax percentages from PDF invoices.
- **File Organization**: Moves processed invoices to a different folder after extraction based on specific conditions.
- **Flexible**: Easily configurable to work with different sets of invoices by modifying regular expressions and folder paths.

## Requirements

- Python 3.x
- `PyPDF2`: A Python library for reading PDF files.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your PDF invoices in the `invoices` folder. Ensure the folder structure is correct and the PDFs are properly formatted.

2. Run the script:

    ```bash
    python3 main.py
    ```

3. The script will:
    - Extract relevant information from each PDF.
    - Print extracted details to the console.
    - /filter_by_number.py to filter by a specific number.
    - Move processed files to the `processed_invoices` folder.

## Regular Expressions

The script uses the following regular expressions to extract information:

- **Invoice Number**: `r'Invoice Number\s+(\S+)'`
- **Bill To**: `r'To:\s+([\s\S]+?)\nHrs/Qty'`
- **Items**: `r'Hrs/Qty\s+Service\s+Rate/Price\s+Adjust\s+([\s\S]+?)\nSub Total'`
- **Notes and Terms**: `r'(?<=Invoice)([\s\S]+?)Page 1/1'`
- **Discount/Tax Percentages**: `r'(\d+\.\d+%)'`



