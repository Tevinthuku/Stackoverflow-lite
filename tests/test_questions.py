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

    def test_user_can_post_a_question(self):
        self.user_login()
        response = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'], [{"title": "What is Dev?",
                                           "creator_id": 1,
                                           "body": "I really like how people talk about Tony's Dev"}])

    # tests if a user enters an invalid token
    def user_enter_invalid_token(self):
        token = "tevlovespython"
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "token is expired or invalid")

    def test_api_v1_questions_response_status_code(self):
        response = self.client.get(
            "/api/v1/questions")
        self.assertEqual(response.status_code, 200)
    # tests that an unregistered user can not post a question

    def test_unregistered_user_not_post_question(self):
        response = self.client.post("api/v1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': ""},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Token is missing")
