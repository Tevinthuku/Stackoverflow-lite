from flask import Flask, jsonify, Blueprint
from app.api.v1.routes.questions import path_1 as questions

from config import app_config


def app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(questions)

    return app
