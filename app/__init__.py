from flask import Flask, jsonify, Blueprint


def app(config_name):
    app = Flask(__name__)

    return app
