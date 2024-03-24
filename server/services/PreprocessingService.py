import os
import cv2
import pytesseract
import numpy as np
from flask import current_app
from pytesseract import Output


class PreprocessingService:
    def preprocess_for_checkboxes(self, resized_image: str):
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 100)
