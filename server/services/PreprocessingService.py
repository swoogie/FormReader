import cv2
import numpy as np
import io


class PreprocessingService:

    def canny(self, resized_image: str, bottom_threshold: int, top_threshold: int):
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, bottom_threshold, top_threshold)
        return edges

    def dilate(self, image, kernel_matrix = 2):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_matrix, kernel_matrix))
        return cv2.dilate(image, kernel, iterations=1)

    def find_and_crop_paper(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blurred, 50, 100)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        paper_contour = None

        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4:
                paper_contour = approx
                break

        image_area = img.shape[0] * img.shape[1]
        paper_contour_area = cv2.contourArea(paper_contour)
        if paper_contour_area < (1/3) * image_area:
            return img

        rect = cv2.minAreaRect(paper_contour)
        width = int(min(rect[1]))
        height = int(max(rect[1]))

        if paper_contour is not None:
            pts1 = np.float32(paper_contour.reshape(-1, 2))
            pts2 = np.float32([[0, 0], [0, height], [width, 0], [width, height]])
            sorted_pts1 = np.zeros_like(pts1)
            for i, pt in enumerate(pts2):
                index = np.argmin(np.sum((pts1 - pt) ** 2, axis=1))
                sorted_pts1[i] = pts1[index]
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            warped = cv2.warpPerspective(img, matrix, (width, height)) 

            return warped
        else:
            return img

    def sharpen(self, img):
        gaussian_blur = cv2.GaussianBlur(img, (5,5), 0)
        sharpened = cv2.addWeighted(img, 1.5, gaussian_blur, -0.5, 0)
        return sharpened

    def resize(self, image, max_size: int): 
        height, width = image.shape[:2]
        if width > height:
            new_width = max_size
            ratio = max_size / width
            new_height = int(height * ratio)
        else:
            new_height = max_size
            ratio = max_size / height
            new_width = int(width * ratio)

        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image, ratio, new_width, new_height

    def encode(self, img):
        ret, buffer = cv2.imencode('.jpg', img)
        if ret:
            return io.BytesIO(buffer.tobytes())
