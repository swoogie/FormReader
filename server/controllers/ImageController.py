from dependency_injector.wiring import inject, Provide
import logging
from flask import request, flash, redirect, jsonify, current_app, send_file
from services import ImageReadingService, \
                     PreprocessingService, \
                     CheckboxDetectionService, \
                     LineDetectionService, \
                     WordDetectionService, \
                     CharInputDetectionService
from container import Container


class ImageController:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_IMAGE_SIZE = 3000

    def handle(self):
        if self._post_valid():
            checkbox_coords, line_coords, char_input_coords, width, height = self.process_image()
            return jsonify({
                'checkbox_coords': checkbox_coords,
                'line_coords': line_coords,
                'char_input_coords': char_input_coords,
                'resolution': [width, height]
            })

    def crop(self):
        if self._post_valid():
            return send_file(self.crop_deskew(), mimetype='image/jpeg')

    @inject
    def process_image(
        self,
        image_reader: ImageReadingService = Provide[Container.image_reader],
        preprocessor: PreprocessingService = Provide[Container.preprocessor],
        checkbox_detector: CheckboxDetectionService = Provide[Container.checkbox_detector],
        line_detector: LineDetectionService = Provide[Container.line_detector],
        word_detector: WordDetectionService = Provide[Container.word_detector],
        char_input_detector: CharInputDetectionService = Provide[Container.char_input_detector]
    ):
        image = image_reader.read_image(request.files['file'])
        cropped = preprocessor.find_and_crop_paper(image)
        sharpened = preprocessor.sharpen(cropped)
        resized, _, width, height = preprocessor.resize(sharpened, self.MAX_IMAGE_SIZE)
        red_zones = word_detector.detect(resized)

        checkbox_coordinates = checkbox_detector.detect(resized)
        line_coordinates = self._filter_overlaps(line_detector.detect(resized), red_zones)
        char_input_coordinates = self._filter_overlaps(char_input_detector.detect(resized), red_zones)

        return self._get_destructured_array(checkbox_coordinates), \
            self._get_destructured_array(line_coordinates), \
            self._get_destructured_array(char_input_coordinates), \
            width, height

    def crop_deskew(
        self,
        image_reader: ImageReadingService = Provide[Container.image_reader],
        preprocessor: PreprocessingService = Provide[Container.preprocessor],
        ):
        image = image_reader.read_image(request.files['file'])
        cropped = preprocessor.find_and_crop_paper(image)
        resized, _, _, _ = preprocessor.resize(cropped, self.MAX_IMAGE_SIZE)
        encoded_image = preprocessor.encode(resized)
        return encoded_image

    def _post_valid(self):
        if request.method == 'POST':
            if 'file' not in request.files:
                logging.warning('testing warning log')
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self._allowed_file(file.filename):
                return True

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in ImageController.ALLOWED_EXTENSIONS

    def _get_original_coords(self, ratio, all_coords):
        response_coords = []
        for coords in all_coords:
            x1, y1, x2, y2 = map(lambda coord: int(coord / ratio), coords)
            response_coords.append([x1, y1, x2, y2])
        return response_coords

    def _get_destructured_array(self, element):
        response = []
        for coords in element:
            x1, y1, x2, y2 = coords
            response.append([int(x1), int(y1), int(x2), int(y2)])
        return response

    def _filter_overlaps(self, coords, red_zones):
        filtered_rects = []
        for rect in coords:
            intersects_box = False
            for box in red_zones:
                if self._intersects(rect, box):
                    intersects_box = True
                    break

            if not intersects_box:
                filtered_rects.append(rect)
        return filtered_rects

    def _intersects(self, line, box):
        line_x1, line_y1, line_x2, line_y2 = line
        box_x, box_y, box_w, box_h = box

        if (box_x <= line_x1 <= box_x + box_w and box_y <= line_y1 <= box_y + box_h) or \
        (box_x <= line_x2 <= box_x + box_w and box_y <= line_y2 <= box_y + box_h):
            return True

        return False