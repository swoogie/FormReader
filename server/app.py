from flask import Flask, render_template
import json
from .controllers import ImageController
from .controllers import VueController
from .container import Container
from .middlewares.LoggingMiddleware import LoggingMiddleware
from logging.config import dictConfig


def create_app() -> Flask:
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'uploads/app.log',
                'formatter': 'default' 
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        }
    })

    container = Container()

    app = Flask(
        __name__,
        template_folder="../client/dist",
        static_folder="../client/dist",
        static_url_path=""
    )
    # print(app.root_path)
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.config.from_file("../flaskConfig.json", load=json.load)
    app.container = container
    app.add_url_rule("/", "vue", VueController(app).vue,
                     methods=["GET", "OPTIONS"])
    app.add_url_rule("/<string:text>", "vue")
    app.add_url_rule("/<path:text>", "vue")
    app.add_url_rule("/image", "handle",
                     ImageController().handle, methods=["GET", "POST", "OPTIONS"])

    return app
