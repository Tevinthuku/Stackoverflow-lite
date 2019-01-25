

from datetime import datetime

QUESTIONS = []
USERS = []


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


class UserModel:
    """
    This is the user model class that contains our model setup
    """

    def __init__(self, firstname, username, lastname, email, password):
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
        self.is_admin = False

    # after sign-up save the user to the created dict , USERS_LEN
    def save_user(self):
        """
        Add a new user to the users store
        """
        USERS.append(self)

    # lets check the data store for any user
    @staticmethod
    def query_users(username, password):
        return [UserModel.to_json(user) for user in USERS if user.username == username and user.password == password]

    # return a json data , a readable dictionary object, including the date user was registered
    @staticmethod
    def to_json(user):
        return {"firstname": user.firstname,
                "lastname": user.lastname,
                "username": user.username,
                "email": user.email,
                "password": user.password,

                "registered_on": user.registered_on, }
