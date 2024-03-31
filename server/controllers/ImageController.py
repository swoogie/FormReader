from dependency_injector.wiring import inject, Provide
import logging
from flask import request, flash, redirect, jsonify, current_app
from services import ImageReadingService, CheckboxDetectionService, LineDetectionService
from container import Container


class ImageController:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_IMAGE_SIZE = 3000

    def handle(self):
        if request.method == 'POST':
            if 'file' not in request.files:
                logging.warning('testing warning log')
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                checkbox_coordinates, input_line_coordinates = self.process_image()
                return jsonify({
                    'checkbox_coordinates': checkbox_coordinates,
                    'input_line_coordinates': input_line_coordinates
                })

    @inject
    def process_image(
        self,
        image_reader: ImageReadingService = Provide[Container.image_reader],
        checkbox_detector: CheckboxDetectionService = Provide[Container.checkbox_detector],
        line_detector: LineDetectionService = Provide[Container.line_detector]
    ):
        resized_image, ratio = image_reader.read_image(request.files['file']).resize_image(ImageController.MAX_IMAGE_SIZE)
        checkbox_coordinates = self._get_original_coords(ratio, checkbox_detector.detect(resized_image))
        before_resize = line_detector.detect(resized_image)
        for line in before_resize:
            current_app.logger.info(line)
        input_line_coordinates = self._get_original_coords(ratio, before_resize)

        return checkbox_coordinates, input_line_coordinates

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower(
            ) in ImageController.ALLOWED_EXTENSIONS

    def _get_original_coords(self, ratio, allCoords):
        response_coords = []
        for coords in allCoords:
            x1, y1, x2, y2 = map(lambda coord: int(coord / ratio), coords)
            response_coords.append([x1, y1, x2, y2])
        return response_coords