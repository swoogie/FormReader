import pytesseract
from services import PreprocessingService


class WordDetectionService:
    CONFIG = '--psm 11'

    def __init__(self, preprocessor: PreprocessingService):
        self.preprocessor = preprocessor

    def detect(self, image):
        edges = self.preprocessor.canny(image, 50, 100)
        # dilated = self.preprocessor.dilate(edges, 2)

        data = pytesseract.image_to_data(edges, output_type=pytesseract.Output.DICT, config=self.CONFIG)

        filtered_boxes = []
        for i in range(len(data['level'])):
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            aspect_ratio = float(w) / h
            if 500 >= w * h:
                continue
            if 1.1 >= aspect_ratio:
                continue
            filtered_boxes.append((x, y, w, h))
        return filtered_boxes
