import pytesseract
from PIL import Image

# 🛠️ Configure Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_file, lang='eng'):
    """
    Extracts text content from an image file using Tesseract OCR with multi-language support.

    Args:
        image_file: A file-like object or image path.
        lang (str): Language(s) for OCR, e.g., 'eng+hin'.

    Returns:
        A string containing the OCR-processed text.
    """
    image = Image.open(image_file).convert("RGB")
    text = pytesseract.image_to_string(image, lang=lang)
    return text
