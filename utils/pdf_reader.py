# utils/pdf_reader.py

import pdfplumber

def read_pdf(file):
    """
    Extracts text from all pages of a PDF file using pdfplumber.

    Args:
        file: A file-like object (e.g., from Streamlit file uploader or a path).

    Returns:
        A single string containing the combined text from all pages.
    """
    text = ""

    # 📖 Open and parse the PDF file
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"  # Add text from each page

    return text
