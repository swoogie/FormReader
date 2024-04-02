from services import PreprocessingService
import cv2


class CheckboxDetectionService:
    CHECKBOX_THRESHOLDS = (50, 150)

    def __init__(self, preprocessor: PreprocessingService):
        self._preprocessor = preprocessor

    def _explore_hierarchy(self, contour_index, hierarchy, contours, last_children):
        if hierarchy[0][contour_index][2] != -1:
            child_index = hierarchy[0][contour_index][2]
            self._explore_hierarchy(child_index, hierarchy, contours, last_children)
        else:
            last_children.append(contours[contour_index])

    def detect(self, resized_image):

        preprocessed_img = self._preprocessor.canny(resized_image, *self.CHECKBOX_THRESHOLDS)

        contours, hierarchy = cv2.findContours(
            preprocessed_img.copy(),
            cv2.RETR_CCOMP,
            cv2.CHAIN_APPROX_SIMPLE
        )

        last_children = []
        squares = []
        for i, contour in enumerate(contours):
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            contour_area = w * float(h)
            if (len(approx) == 4 and 0.9 <= aspect_ratio <= 1.1 and 1000 <= contour_area <= 3000):
                self._explore_hierarchy(i, hierarchy, contours, last_children)
                for rect in last_children:
                    x, y, w, h = cv2.boundingRect(rect)
                    squares.append((x, y, x + w, y + h))

        grouped_rectangles, weights = cv2.groupRectangles(
            squares, groupThreshold=1, eps=0.03)

        return grouped_rectangles
