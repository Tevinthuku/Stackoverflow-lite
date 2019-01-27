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
                             "username": "tony",
                             "email": "blair1234.dev@gmail.com",
                             "password": "Blairman1234",
                             "confirm_password": "Blairman1234"}
        self.signup_user3 = {
            "firstname": "Third",
            "lastname": "Avenger",
            "username": "thor",
            "email": "valhalla.dev@gmail.com",
            "password": "Valhallla123",
            "confirm_password": "Valhallla123"
        }

        self.login_user_1 = {"username": "tevothuku",
                             "password": "Barca123"}
        self.login_user_2 = {"username": "tony", "password": "Blairman1234"}
        self.login_user_3 = {"username": "thor", "password": "Valhallla123"}
        self.post_question1 = {"title": "What is Dev?",
                               "creator_id": 1,
                               "body": "I really like how people talk about Tony's Dev"}
        self.post_question2 = {"title": "Question 2",
                               "creator_id": 1,
                               "body": "This is question 2"}
        self.post_question3 = {"title": "Question 3",
                               "creator_id": 1,
                               "body": "This is question 3"}
        self.answer_to_question1 = {"answer": "I believe its...."}
        self.answer_to_question2 = {"answer": "I think the answer is ..."}
        self.broken_answer = {"ans": "No its not"}
        self.token = ""
        self.token2 = ""
        self.token3 = ""
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestQuestionsApiEndpoint(RoutesBaseTest):
    def user_login(self):
        # login user1
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user1),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_1),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        # login user2
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user2),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_2),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token2 = data["token"]
        # login user3
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user3),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user_3),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token3 = data["token"]

    # test an answer being posted

    def test_user_post_answer(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        response = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], [{'answer': 'I believe its....'}])
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    # test posting answer that doesnt exist
    def test_post_answer_to_non_existent_question(self):
        self.user_login()
        response = self.client.post(
            "api/v1/questions/100/answers", data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_answer_with_improperparams(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        res = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.broken_answer), headers={'x-access-token': self.token2}, content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 400)
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    def test_question_creator_can_upvote_answer(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        response = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], [{'answer': 'I believe its....'}])
        upvotequery = self.client.put("api/v1/questions/{}/answers/{}".format(questionId, 0), data=json.dumps(
            {"newanswer": "Upvoting"}), headers={'x-access-token': self.token}, content_type="application/json")
        upvoteresponse = json.loads(upvotequery.data.decode("utf-8"))
        self.assertEqual(upvoteresponse["status"], 200)
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    def test_answerupdate_by_responder(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        response = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], [{'answer': 'I believe its....'}])
        updateanswerquery = self.client.put("api/v1/questions/{}/answers/{}".format(questionId, 0), data=json.dumps(
            {"newanswer": "Upvoting"}), headers={'x-access-token': self.token2}, content_type="application/json")
        upvoteresponse = json.loads(updateanswerquery.data.decode("utf-8"))
        self.assertEqual(upvoteresponse["status"], 200)
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    def test_updateanswer_with_wrong_params(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        response = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], [{'answer': 'I believe its....'}])
        updateanswerquery = self.client.put("api/v1/questions/{}/answers/{}".format(questionId, 0), data=json.dumps(
            {"newaner": "Wrong param"}), headers={'x-access-token': self.token2}, content_type="application/json")
        upvoteresponse = json.loads(updateanswerquery.data.decode("utf-8"))
        self.assertEqual(upvoteresponse["status"], 400)
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")

    def test_wrong_user_trying_update(self):
        self.user_login()
        quest = self.client.post("api/v1/questions", data=json.dumps(
            self.post_question1), headers={'x-access-token': self.token}, content_type="application/json")
        questres = json.loads(quest.data.decode('utf-8'))
        questionId = questres["data"][0].get("question_id")
        response = self.client.post(
            "api/v1/questions/{}/answers".format(questionId), data=json.dumps(
                self.answer_to_question1), headers={'x-access-token': self.token2}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], [{'answer': 'I believe its....'}])
        updateanswerquery = self.client.put("api/v1/questions/{}/answers/{}".format(questionId, 0), data=json.dumps(
            {"newanswer": "Wrong param"}), headers={'x-access-token': self.token3}, content_type="application/json")
        upvoteresponse = json.loads(updateanswerquery.data.decode("utf-8"))
        self.assertEqual(upvoteresponse["status"], 401)
        response = self.client.delete(
            "api/v1/questions/{}".format(questionId), headers={'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], "Deleted successfully")
