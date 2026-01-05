import pytesseract
from PIL import Image, ImageOps

# image = Image.open('src/data/raw/image.png')
# grey_image = ImageOps.grayscale(image)

def extract_text(image):
    return pytesseract.image_to_string(image,config='--psm 1').strip()

# if __name__=='__main__':
#     text = extract_text(image)
#     print(text)