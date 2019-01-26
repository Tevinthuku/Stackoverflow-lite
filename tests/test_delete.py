import json
import unittest

from app import app


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()

        self.signup_user1 = {"firstname": "Tevin",
                             "lastname": "Gachagua",
                             "username": "tevothuku",
                             "email": "tev@gmail.com",
                             "password": "Barca123",
                             "confirm_password": "Barca123"}

        self.signup_user2 = {"firstname": "Tony",
                             "lastname": "Andela",
                             "username": "fakeadmin",
                             "email": "blair1234.dev@gmail.com",
                             "password": "Blairman1234",
                             "confirm_password": "Blairman1234"}

        self.login_user_1 = {"username": "tevothuku",
                             "password": "Barca123"}

        self.post_question1 = {"title": "What is Dev?",
                               "creator_id": 1,
                               "body": "I really like how people talk about Tony's Dev"}
        self.post_question2 = {"title": "Question 2",
                               "creator_id": 1,
                               "body": "This is question 2"}
        self.post_question3 = {"title": "Question 3",
                               "creator_id": 1,
                               "body": "This is question 3"}
        self.answer_to_question2 = {"answer": "I think the answer is ..."}
        self.token = ""
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestQuestionsApiEndpoint(RoutesBaseTest):
    def user_login(self):
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user1),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_1),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]

    # tests that an unregistered user can not post a question

    def test_user_deleting_question(self):
        self.user_login()
        self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        response = self.client.delete(
            "api/v1/questions/1", headers={'x-access-token': self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    def test_non_user_deleting_question(self):
        response = self.client.delete(
            "api/v1/questions/1", headers={'x-access-token': self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Token is missing")

    def test_delete_non_existent_question(self):
        self.user_login()
        response = self.client.delete(
            "api/v1/questions/12", headers={'x-access-token': self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "This question doesn't exist")
