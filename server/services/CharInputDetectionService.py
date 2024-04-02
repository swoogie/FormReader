from services import PreprocessingService
import cv2

class CharInputDetectionService:

    def __init__(self, preprocessor: PreprocessingService):
        self._preprocessor = preprocessor

    def detect(self, image, red_zones):
        edges = self._preprocessor.canny(image, 5, 15)

        rectangles = []
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            contour_area = w * float(h)
            if (0.7 <= aspect_ratio <= 0.9 and contour_area > 2000):
                rectangles.append((x, y, x + w, y + h))

        filtered_rects = []
        for rect in rectangles:
            intersects_box = False
            for box in red_zones:
                if self._intersects(rect, box):
                    intersects_box = True
                    break

            if not intersects_box:
                filtered_rects.append(rect)

        return filtered_rects

    def _intersects(self, element, box):
        line_x1, line_y1, line_x2, line_y2 = element
        box_x, box_y, box_w, box_h = box

        if (box_x <= line_x1 <= box_x + box_w and box_y <= line_y1 <= box_y + box_h) or \
        (box_x <= line_x2 <= box_x + box_w and box_y <= line_y2 <= box_y + box_h):
            return True

        return False
