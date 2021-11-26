from lib.api.v1 import avengers_controller

from flask import Flask
from flask_cors import CORS


def create_app():
    """
    Return the flask app instance after initializing the app and registering the V1 blueprints
    """
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(avengers_controller.v1_avengers_bp)

    return app
