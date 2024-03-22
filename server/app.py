from flask import Flask, render_template
import json
from .controllers import ImageController
from .controllers import VueController
from .container import Container
from .middlewares.LoggingMiddleware import LoggingMiddleware


def create_app() -> Flask:
    container = Container()

    app = Flask(
        __name__,
        template_folder="../client/dist",
        static_folder="../client/dist",
        static_url_path=""
    )
    print(app.root_path)
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
