"""All routes pertaining to questions"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.model import QuestionModel


@path_1.route("/questions", methods=['GET'])
def get_all_questions():
    """
    User to fetch all questions ever recorded
    """
    questions = QuestionModel.get_all_questions()
    if questions:
        return jsonify({"status": 200, "data": questions}), 200
    return jsonify({"status": 200, "data": []}), 200
