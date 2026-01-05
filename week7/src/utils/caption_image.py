from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
# from src.utils.caption_image import Captionize

class Captionize:
    def __init__(self):
        # loading BLIP processor and model
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base",use_fast=True)
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def generate_caption(self,image):
        # generating caption 
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        return caption
    

# image = Image.open('src/data/raw/image.png')

# caption = Captionize().generate_caption(image)
# print(caption)