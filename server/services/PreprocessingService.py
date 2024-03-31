import cv2


class PreprocessingService:
    def canny(self, resized_image: str, bottom_threshold: int, top_threshold: int):
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, bottom_threshold, top_threshold)
        return edges
