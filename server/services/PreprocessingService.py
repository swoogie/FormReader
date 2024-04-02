import cv2


class PreprocessingService:

    def canny(self, resized_image: str, bottom_threshold: int, top_threshold: int):
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, bottom_threshold, top_threshold)
        return edges

    def dilate(self, image, kernel_matrix = 2):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_matrix, kernel_matrix))
        return cv2.dilate(image, kernel, iterations=1)

    def crop(self, edges, img):
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        imgHeight, imgWidth = img.shape[:2]
        image_area = imgHeight * imgWidth
        bounding_rect_area = w * h

        if bounding_rect_area > (1/3) * image_area:
            cropped_img = img[y:y+h, x:x+w]
            return cropped_img
        return img 

    def resize_image(self, max_size: int): 
        height, width = self.image.shape[:2]
        if width > height:
            new_width = max_size
            ratio = max_size / width
            new_height = int(height * ratio)
        else:
            new_height = max_size
            ratio = max_size / height
            new_width = int(width * ratio)

        resized_image = cv2.resize(self.image, (new_width, new_height))
        return resized_image, ratio

    def deskew(self):
        raise NotImplementedError