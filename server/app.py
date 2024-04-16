from flask import Flask
import os
from controllers import ImageController, VueController
from container import Container
from logger import getLoggerConfig
import logging.config


def create_app() -> Flask: 
    logging.config.dictConfig(getLoggerConfig())

    container = Container()

    app = Flask(
        __name__,
        template_folder="../client/dist",
        static_folder="../client/dist",
        static_url_path=""
    )
    app.config.from_prefixed_env()
    app.container = container
    app.add_url_rule("/", "vue", VueController(app).vue,
                     methods=["GET", "OPTIONS"])
    app.add_url_rule("/<string:text>", "vue")
    app.add_url_rule("/<path:text>", "vue")
    app.add_url_rule("/image", "handle",
                     ImageController().handle, methods=['POST'])
    app.add_url_rule("/crop", "crop",
                     ImageController().crop, methods=['POST'])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))