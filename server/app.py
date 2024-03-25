from flask import Flask, render_template
import json
import os
from .controllers import ImageController
from .controllers import VueController
from .container import Container
from .middlewares.LoggingMiddleware import LoggingMiddleware
import logging.config


def create_app() -> Flask: 
    with open('logger.config.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)

    container = Container()

    app = Flask(
        __name__,
        template_folder="../client/dist",
        static_folder="../client/dist",
        static_url_path=""
    )
    # print(app.root_path)
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.config.from_file("../flask.config.json", load=json.load)
    app.container = container
    app.add_url_rule("/", "vue", VueController(app).vue,
                     methods=["GET", "OPTIONS"])
    app.add_url_rule("/<string:text>", "vue")
    app.add_url_rule("/<path:text>", "vue")
    app.add_url_rule("/image", "handle",
                     ImageController().handle, methods=["GET", "POST", "OPTIONS"])

    return app
