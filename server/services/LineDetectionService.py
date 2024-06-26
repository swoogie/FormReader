from services import PreprocessingService
import cv2
import numpy as np


class LineDetectionService:

    def __init__(self, preprocessor: PreprocessingService):
        self._preprocessor = preprocessor

    def _filter_overlapping_lines(self, lines, height):
        filtered_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if (y1 - 10 < 0 or y1 + 10 > height):
                continue
            overlaps = False
            for existing_line in filtered_lines:
                ex1, ey1, ex2, ey2 = existing_line
                if abs(y1 - ey2) > 50:
                    continue
                if (x2 < ex1 or x1 > ex2):
                    continue
                overlaps = True
                break
            if not overlaps:
                filtered_lines.append((x1, y1, x2, y2))

        return filtered_lines 

    def detect(self, resized_image):
        preprocessed_image = self._preprocessor.canny(resized_image, 50, 100)
        height, _ = resized_image.shape[:2]

        dilated_image = self._preprocessor.dilate(preprocessed_image, 2, 3)
        eroded_image = self._preprocessor.erode(dilated_image, 2, 3)
        lines = cv2.HoughLinesP(eroded_image, 1, np.pi/180, threshold=300, minLineLength=50, maxLineGap=3)
        vertical_lines = filter(lambda line: abs(line[0][3] - line[0][1]) < 5, lines)
        sorted_lines = sorted(vertical_lines, key=lambda line: line[0][1])

        return self._filter_overlapping_lines(sorted_lines, height)
