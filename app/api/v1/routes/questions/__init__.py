"""All routes pertaining to questions"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.model import QuestionModel, AnswerModel, QUESTIONS
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
                        'error': "Check your json keys. Should be topic and body"})

    question = QuestionModel(title=title,
                             body=body,
                             creator_id=userId)

    question.save_question()

    return jsonify({"status": 201,
                    "data": [{"title": title,
                              "creator_id": userId,
                              "question_id": len(QUESTIONS)-1,
                              "body": body}]}), 201


@path_1.route("/questions/<int:question_id>/answers", methods=["POST"])
@token_required
def create_new_answer(specific_user, question_id):
    userId = specific_user.get("user_id")
    try:
        data = request.get_json()
        answer = data['answer']
    except:
        return jsonify({"status": 400,
                        "error": "Check your json keys. answer should be present"})

    try:
        question = QuestionModel.get_question_object(question_id)[0]
        answerlen = len(vars(question).get("answers", []))
        newanswer = AnswerModel(
            answer=answer, question_id=question_id, creator_id=userId, answerId=answerlen)
    except IndexError:
        return jsonify({"status": 401, "data": "This question doesn't exist"}), 401
    question.save_answer(newanswer)
    return jsonify({"status": 201, "data": [{
        "answer": answer
    }]})


@path_1.route("/questions/<int:question_id>/answers/<int:answer_id>", methods=["PUT"])
@token_required
def detect_app(specific_user, question_id, answer_id):
    userId = specific_user.get("user_id")
    try:
        data = request.get_json()
        newanswer = data['newanswer']

    except:
        return jsonify({"status": 400,
                        "error": "Check your json keys. the new answer should be present"})

    try:
        question = QuestionModel.get_question_object(question_id)[0]
    except IndexError:
        return jsonify({"status": 401, "data": "This question doesn't exist"}), 401
    answobj = question.get_answer_object(answer_id)
    if userId == vars(answobj[0]).get("creator_id", ""):
        question.update_answer(newanswer, answer_id)
        return jsonify({
            "status": 200,
            "data": "Updated comment successfully"
        }), 200
    elif userId == question.creator_id:
        question.upvote_answer(answer_id)
        return jsonify({
            "status": 200,
            "data": "Upvoted answer"
        }), 200
    else:
        return jsonify({
            "status": 401,
            "data": "Permission denied"
        }), 401


@path_1.route("/questions/<int:question_id>", methods=['DELETE'])
@token_required
def delete_question(specific_user, question_id):
    userId = specific_user.get("user_id")

    try:
        question = QuestionModel.get_question(question_id)[0]
    except IndexError:
        return jsonify({"status": 401, "data": "This question doesn't exist"}), 401
    if question.get("creator_id", "") == userId:
        deleted = QuestionModel.deletequestion(question_id)
        if deleted:
            return jsonify({'status': 200, 'data': "Deleted successfully"}), 200
        return jsonify({'status': 404, 'data': "Question with id {} not found".format(question_id)}), 404

    if question.get("creator_id", "") != userId:
        return jsonify({"status": 401, "data": "This question isn't yours"}), 401


@path_1.route("/questions/<int:question_id>", methods=['GET'])
def get_specific_question(question_id):
    """
    User to fetch specific question
    """
    question = QuestionModel.get_question(question_id)
    if question:
        return jsonify({"status": 200, "data": question}), 200
    return jsonify({"status": 404, "data": "We cant find this question"}), 404
