from dependency_injector.wiring import inject, Provide
import logging
import os
from flask import request, flash, redirect, url_for, jsonify, make_response, current_app
from werkzeug.utils import secure_filename
from ..services import PreprocessingService
from ..container import Container


class ImageController:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    @inject
    def handle(self, preprocessor: PreprocessingService = Provide[Container.preprocessor]):
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
                filename = secure_filename(file.filename)
                save_path = os.path.join(
                    current_app.root_path, 
                    current_app.config['UPLOAD_FOLDER'],
                    filename
                )
                file.save(save_path)
                # return redirect(url_for('download_file', name=filename))
            return jsonify({'message': preprocessor.preprocess("check uploads")})

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ImageController.ALLOWED_EXTENSIONS
