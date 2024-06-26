from services import PreprocessingService
import cv2

class CharInputDetectionService:

    def __init__(self, preprocessor: PreprocessingService):
        self._preprocessor = preprocessor

    def detect(self, image):
        edges = self._preprocessor.canny(image, 10, 15)
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            contour_area = w * float(h)
            if (0.7 <= aspect_ratio <= 0.9 and 1000 <= contour_area <= 4000):
                rectangles.append((x, y, x + w, y + h))

        return rectangles
