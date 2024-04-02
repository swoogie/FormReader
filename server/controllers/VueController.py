from dependency_injector.wiring import inject, Provide
import logging
import os
from flask import request, flash, redirect, url_for, jsonify, make_response, render_template
from werkzeug.utils import secure_filename
from services import PreprocessingService
from container import Container
from controllers import ImageController


class VueController:

    def __init__(self, app):
        self.app = app

    def vue(self, text=None):
        self.app.logger.info(f"index.html - {text}")
        if request.method == 'GET':
            return self.app.send_static_file('index.html')

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ImageController.ALLOWED_EXTENSIONS

    def _build_cors_preflight_response(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    def _corsify_actual_response(self, response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Credentials", "*")
        return response
