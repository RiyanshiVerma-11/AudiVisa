# utils/image_captioner.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# 🌟 Lazy-loaded processor and model (only initialized once)
processor = None
model = None

def load_model():
    """
    Load the BLIP image captioning model and processor if not already loaded.
    This ensures models are not reloaded unnecessarily.
    """
    global processor, model
    if processor is None or model is None:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_image_caption(image_file):
    """
    Generates a caption for the provided image file using BLIP.
    
    Args:
        image_file: A file-like object or path to an image file.
    
    Returns:
        A string caption describing the image content.
    """
    load_model()
    
    # 🖼️ Open image and convert to RGB
    image = Image.open(image_file).convert('RGB')
    
    # 📦 Prepare image for the model
    inputs = processor(image, return_tensors="pt")
    
    # 🔮 Generate caption without computing gradients (no training)
    with torch.no_grad():
        output = model.generate(**inputs)
    
    # 📝 Decode and return the generated caption
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
