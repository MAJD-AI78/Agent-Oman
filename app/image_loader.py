from PIL import Image
import pytesseract

def load_image_text(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image)
