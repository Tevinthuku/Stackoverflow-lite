

from datetime import datetime

QUESTIONS = []
USERS = []


class AnswerModel:
    def __init__(self, answer, question_id, creator_id):
        """
        Constructor of the answer class
        """
        self.answer = answer
        self.question_id = question_id
        self.creator_id = creator_id,
        self.accepted = False

    @staticmethod
    def to_json(answer):
        return {
            "answer": answer.answer,
            "question_id": answer.question_id,
            "creator_id": answer.creator_id,
            "accepted": answer.accepted
        }

    def save_answer(self):
        for idx, question in enumerate(QUESTIONS):
            if vars(question).get("question_id") == self.question_id:
                newanswers = vars(question).get(
                    "answers", []).append(self)
                vars(question).update(answers=newanswers)
                QUESTIONS[idx] = question


class QuestionModel:
    def __init__(self, title, body, creator_id):
        """
        Constructor of the questions class
        """
        self.question_id = len(QUESTIONS)+1
        self.title = title
        self.body = body
        self.creator_id = creator_id
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
            "answers": [vars(answer) for answer in question.answers],
            "creator_id": question.creator_id
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

    @staticmethod
    def deletequestion(question_id):
        found = None
        for question in QUESTIONS:
            if question.question_id == question_id:
                QUESTIONS.remove(question)
                found = True
            elif question.question_id != question_id:
                found = False
        return found


class UserModel:
    """
    This is the user model class that contains our model setup
    """

    def __init__(self, firstname, username, lastname, email, password, is_admin=False):
        """
        Start by defining each user attributes to use during the tests
        Keep in mind the user is not an admin
        """
        self.user_id = len(USERS)+1
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.registered_on = datetime.now()
        self.password = password
        self.is_admin = is_admin

    # after sign-up save the user to the created dict , USERS_LEN
    def save_user(self):
        """
        Add a new user to the users store
        """
        USERS.append(self)

    # lets check the data store for any user
    @staticmethod
    def query_users(username, password):
        return [UserModel.login_to_json(user) for user in USERS if user.username == username and user.password == password]

    # return a json data , a readable dictionary object, including the date user was registered
    @staticmethod
    def to_json(user):
        return {"firstname": user.firstname,
                "lastname": user.lastname,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "is_admin": user.is_admin,
                "registered_on": user.registered_on}

    @staticmethod
    def login_to_json(user):
        return {
            "username": user.username,
            "password": user.password
        }
