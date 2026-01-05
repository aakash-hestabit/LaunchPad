from PIL import Image
from pdf2image import convert_from_path
import os


# the problem witht this method of loading the image is this that we are considering the page as an image meaning wvwry page is treated as images and 
# every page goes through OCR BLIP and CLIP making the process very very slow so i have used a hybrid approach while ingesting the image that is also discussed in MULTIMODAL-RAG.md
def load_images(path):
    images = []

    if path.endswith(".pdf"):
        pages = convert_from_path(path)
        for i, page in enumerate(pages):
            images.append((page, {"page":i+1}))
    else:
        img = Image.open(path).convert('RGB')
        images.append((img,{}))
    
    return images