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

        self.signup_user2 = {"firstname": "Yuppy",
                             "lastname": "Maann",
                             "username": "teamlead",
                             "email": "team.dev@gmail.com",
                             "password": "Teamlead1234",
                             "confirm_password": "Teamlead1234"}

        self.login_user_1 = {"username": "tevothuku",
                             "password": "Barca123"}
        self.login_user_2 = {"username": "teamlead",
                             "password": "Teamlead1234"}

        self.post_question1 = {"title": "What is a polymorph?",
                               "creator_id": 1,
                               "body": "Im struggling to get by linear algebra, can anyone help out with this"}

        self.titleless_question = {
            "body": "How do you create a set"
        }

        self.answer_to_question2 = {"answer": "I think the answer is ..."}
        self.wrong_answer = {"ans": ""}
        self.token = ""
        self.token2 = ""
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestQuestionsApiEndpoint(RoutesBaseTest):
    def user_login(self):
        # user 1
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user1),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_1),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        # user 2
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user2),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_2),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        print(data)
        self.token2 = data["token"]

    # tests if a user enters an invalid token
    def user_enter_invalid_token(self):
        token = "tevlovespython"
        response = self.client.post("api/v1/questions",
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

    def test_getting_question_that_isnt_present(self):
        self.user_login()
        getquestion = self.client.get("/api/v1/questions/10")
        self.assertEqual(getquestion.status_code, 404)

    def test_tittleless_question(self):
        self.user_login()
        response = self.client.post("api/v1/questions",
                                    data=json.dumps(self.titleless_question),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["error"], "Check your json keys. Should be topic and body")

    def test_user_trying_to_delete_questionnot_made(self):
        self.user_login()
        response = self.client.post("api/v1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        questionId = result["data"][0].get("question_id")
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token2}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "This question isn't yours")
        self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
