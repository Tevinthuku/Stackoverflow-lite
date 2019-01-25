

from datetime import datetime

QUESTIONS = []


class QuestionModel:
    def __init__(self, title, body):
        """
        Constructor of the questions class
        """
        self.question_id = len(QUESTIONS)+1
        self.title = title
        self.body = body
        self.answers = []
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        QUESTIONS.append(self)

    @staticmethod
    def to_json(question):
        """
        format question object to a readable dictionary
        """
        return {
            "question_id": question.question_id,
            "title": question.title,
            "body": question.body,
            "answers": question.answers
        }

    @staticmethod
    def get_question(question_id):
        """
        fetch a specific question via its id
        """
        return [QuestionModel.to_json(question) for question in QUESTIONS if question.question_id == question_id]

    @staticmethod
    def get_all_questions():
        """
        user get all questions that have ever been asked
        """
        return [QuestionModel.to_json(question) for question in QUESTIONS]
