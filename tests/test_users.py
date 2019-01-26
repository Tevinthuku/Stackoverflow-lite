"""Tests for the user endpoints"""

import unittest
import json

from app import app


class UserBaseTest(unittest.TestCase):
    """
    Set up the user tests
    """

    def setUp(self):
        """
        lets declare the variables to use on the tests
        """
        self.app = app("testing")
        self.client = self.app.test_client()

        self.signup_user1 = {"firstname": "Tevin",
                             "lastname": "Thuku",
                             "username": "tevothuku",
                             "email": "tevinthuku@gmail.com",
                             "password": "Tev54321",
                             "confirm_password": "Tev54321"}

        self.signup_user2 = {"firstname": "Lionel",
                             "lastname": "Messi",
                             "username": "limesi",
                             "email": "limesi@gmail.com",
                             "password": "Limesi1234",
                             "confirm_password": "Limesi123"}

        self.signup_user3 = {"firstname": "Joshua",
                             "lastname": "Ariga",
                             "username": "arigajosh",
                             "email": "ariga@.com",
                             "password": "Ariga123",
                             "confirm_password": "Ariga123"}

        self.signup_user4 = {"firstname": "Codeman",
                             "lastname": "Pragmatic",
                             "username": "codeprag",
                             "email": "codeman@gmail.com",
                             "password": "Code",
                             "confirm_password": "Code"}

        self.signup_user5 = {"firstname": "Codeman",
                             "lastname": "Pragmatic",
                             "username": "codeprag",
                             "email": "codeman@gmail.com",
                             "password": "Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd",
                             "confirm_password": "Codedsdscfsdfsfsfhchdfgvdyvhgsdvghsd"}

        self.signup_user6 = {"firstname": "usersix",
                             "lastname": "Usersixlastname",
                             "username": "six",
                             "email": "usersix@gmail.com",
                             "password": "@Usersix-password",
                             "confirm_password": "@Usersix-password"}

        self.signup_user7 = {"firstname": "Joshua",
                             "lastname": "Ariga",
                             "username": "arigajosh",
                             "email": "ariga@gmail",
                             "password": "Ariga123",
                             "confirm_password": "Ariga123"}

        self.signup_user8 = {"firstname": "Fellowone",
                             "lastname": "lastnamefellow",
                             "username": "fellow",
                             "email": "fellow.dev@gmail.com",
                             "password": "fellowPassword100",
                             "confirm_password": "fellowPassword100"}

        self.login_user1 = {"username": "tevothuku",
                            "password": "tev54321"}

        self.login_user2 = {"username": "limesi",
                            "password": "Limesi1234"}

        self.login_user3 = {"username": "kenyaa",
                            "password": "@Mitcoder1"}

        self.login_user8 = {"username": "fellow",
                            "password": "fellowPassword100"}

    # clean up the tests
    def tearDown(self):
        self.app.testing = False

# testing for the users endpoints


class TestUsersEndpoints(UserBaseTest):

    def test_user_can_sign_up(self):
        """
        Tests to confirm a user signup successfully
        """
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user1), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], "User Registered Successfully!")

    # tests that user sign-up passwords match
    def test_user_enter_unmatching_passwords(self):
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user2), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "Your passwords don't match!")

    # tests user enter wrong email
    def test_user_enter_wrong_email1(self):
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user3), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "Email is Invalid")

    # tests user enter short password
    def test_user_enter_short_password(self):
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user4), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result["error"], "Password should not be less than 8 characters or exceed 20")

    # tests user enter long password
    def test_user_enter_long_password(self):
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user5), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result["error"], "Password should not be less than 8 characters or exceed 20")

    def test_user_enter_wrong_email2(self):
        response = self.client.post(
            "api/v1/auth/signup", data=json.dumps(self.signup_user7), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "Email is Invalid")

    def test_that_user_can_successfully_login(self):
        """
        Test user can login after signup
        """
        self.client.post("api/v1/auth/signup",
                         data=json.dumps(self.signup_user8),
                         content_type="application/json")
        response = self.client.post("api/v1/auth/login",
                                    data=json.dumps(self.login_user8),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['token'])
        self.assertEqual(result["message"], "You have Logged in Successfully")

    # tests no login for unregistered user
    def test_user_no_login_if_not_registered(self):
        """
        Test that an unregistered user can not login
        """
        response = self.client.post("api/v1/auth/login",
                                    data=json.dumps(self.login_user2),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], "Please Register First to Login")
