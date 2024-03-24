import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from pytesseract import Output

class PreprocessingService:
    def read(self, img_file):
        in_memory_file = io.BytesIO(image_file.read())
        img_array = np.array(bytearray(in_memory_file.read()), dtype=np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    def preprocess(self, img: str):
        return img