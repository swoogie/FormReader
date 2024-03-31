from services import PreprocessingService
import cv2
import pytesseract
import numpy as np
import pytesseract


class LineDetectionService:

    def __init__(self, preprocessor: PreprocessingService):
        self._preprocessor = preprocessor

    def _detect_words(self, preprocessed_image):
        data = pytesseract.image_to_data(preprocessed_image, output_type=pytesseract.Output.DICT, config='--psm 11')
        filtered_boxes = []
        for i in range(len(data['level'])):
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            confidence = int(data['conf'][i])
            if 500 >= w * h:
                continue
            aspect_ratio = float(w) / h
            if 1.1 >= aspect_ratio:
                continue
            if 1 > confidence: 
                continue
            filtered_boxes.append((x, y, w, h))

        return filtered_boxes

    def _filter_overlapping_lines(self, lines):
        filtered_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            overlaps = False
            for existing_line in filtered_lines:
                ex1, ey1, ex2, ey2 = existing_line
                if abs(y1 - ey2) > 50:
                    continue
                if (x2 - 10 < ex1 or x1 + 10 > ex2):
                    continue
                overlaps = True
                break
            if not overlaps:
                filtered_lines.append(line[0])

        return filtered_lines 

    def _line_intersects_box(self, line, box):
        line_x1, line_y1, line_x2, line_y2 = line
        box_x, box_y, box_w, box_h = box

        if (box_x <= line_x1 <= box_x + box_w and box_y <= line_y1 <= box_y + box_h) or \
        (box_x <= line_x2 <= box_x + box_w and box_y <= line_y2 <= box_y + box_h):
            return True

        return False

    def detect(self, resized_image):
        preprocessed_image = self._preprocessor.canny(resized_image, 50, 150)

        word_boxes = self._detect_words(preprocessed_image)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated_image = cv2.dilate(preprocessed_image, kernel, iterations=1)
        lines = cv2.HoughLinesP(dilated_image, 1, np.pi/180, threshold=200, minLineLength=50, maxLineGap=3)
        vertical_lines = filter(lambda line: abs(line[0][3] - line[0][1]) < 3, lines)

        aggregated_lines = self._filter_overlapping_lines(vertical_lines)

        filtered_lines = []
        for line in aggregated_lines:
            intersects_box = False
            for box in word_boxes:
                if self._line_intersects_box(line, box):
                    intersects_box = True
                    break

            if not intersects_box:
                filtered_lines.append(line)

        return filtered_lines
