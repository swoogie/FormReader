import cv2
import pytesseract
import numpy as np
import os
from flask import current_app
from pytesseract import Output


class CheckboxDetectionService:
    def detect(self, preprocessed_img, original_img, ratio):
        rectangles = []
        contours, hierarchy = cv2.findContours(
            preprocessed_img.copy(),
            cv2.RETR_CCOMP,
            cv2.CHAIN_APPROX_SIMPLE
        )
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

        response_coords = [];
        for rect in grouped_rectangles:
            x1, y1, x2, y2 = map(lambda coord: int(coord / ratio), rect)
            response_coords.append([x1, y1, x2, y2])
            cv2.rectangle(original_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        try:
            cv2.imwrite('server/uploads/image.png', original_img)
            return response_coords
        except Exception as e:
            print(e)

    def _explore_hierarchy(self, contour_index, hierarchy, contours, last_children):
        if hierarchy[0][contour_index][2] != -1:
            child_index = hierarchy[0][contour_index][2]
            self._explore_hierarchy(child_index, hierarchy, contours, last_children)
        else:
            last_children.append(contours[contour_index])
