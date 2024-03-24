import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from pytesseract import Output

class CheckboxDetectionService:
    def detect(self, preprocessed_img, original_img):
        rectangles = []
        contours, hierarchy = cv2.findContours(
            preprocessed_img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        last_children = []

        for i, contour in enumerate(contours):
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            contour_area = cv2.contourArea(contour)
            if (len(approx) == 4 and 0.9 <= aspect_ratio <= 1.1 and 1000 <= contour_area <= 3000):
                self._explore_hierarchy(i, hierarchy, contours, last_children)
                for rect in last_children:
                    x, y, w, h = cv2.boundingRect(rect)
                    rectangles.append((x, y, x + w, y + h))

        grouped_rectangles, weights = cv2.groupRectangles(
            rectangles, groupThreshold=1, eps=0.03)

        for rect in grouped_rectangles:
            x1, y1, x2, y2 = rect
            cv2.rectangle(original_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        cv2.imwrite('../uploads/image.png', original_img)

    def _explore_hierarchy(contour_index, hierarchy, contours, last_children):
        # Check if the contour has a child
        if hierarchy[0][contour_index][2] != -1:
            child_index = hierarchy[0][contour_index][2]
            explore_hierarchy(child_index, hierarchy, contours, last_children)
        else:
            last_children.append(contours[contour_index])
