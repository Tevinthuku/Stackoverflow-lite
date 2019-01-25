import os
from flask import jsonify
from app import app


config_name = "development"
app = app(config_name)


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"a welcome message": "Welcome to Stackoverflowlite V1 API",
                    })


if __name__ == '__main__':
    app.run(debug=True)
