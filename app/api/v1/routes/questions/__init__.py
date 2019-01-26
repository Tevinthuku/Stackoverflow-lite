"""All routes pertaining to questions"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.model import QuestionModel, QUESTIONS
from app.utils import token_required, decode_token


@path_1.route("/questions", methods=['GET'])
def get_all_questions():
    """
    User to fetch all questions ever recorded
    """
    questions = QuestionModel.get_all_questions()
    if questions:
        return jsonify({"status": 200, "data": questions}), 200
    return jsonify({"status": 200, "data": []}), 200


@path_1.route("/questions", methods=['POST'])
@token_required
def create_question(specific_user):
    userId = specific_user.get("user_id")
    try:
        data = request.get_json()
        title = data['title']
        body = data['body']

    except:
        return jsonify({'status': 400,
                        ' error': "Check your json keys. Should be topic and body"})

    if not title:
        return jsonify({'status': 400,
                        'error': 'topic field is required'})

    if not body:
        return jsonify({'status': 400,
                        'error': 'body field is required'})

    question = QuestionModel(title=title,
                             body=body,
                             creator_id=userId)

    question.save_question()

    return jsonify({"status": 201,
                    "data": [{"title": title,
                              "creator_id": userId,
                              "question_id": len(QUESTIONS),
                              "body": body}]}), 201


@path_1.route("/questions/<int:question_id>", methods=['GET'])
def get_user_get_all_questions_for_a_meetup(question_id):
    """
    User to fetch specific question
    """
    question = QuestionModel.get_question(question_id)
    if question:
        return jsonify({"status": 200, "data": question}), 200
    return jsonify({"status": 404, "data": "We cant find a question for this meetup. No question posted yet"}), 404
