import json
import unittest

from app import app


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()

    def test_api_v1_questions_response_status_code(self):
        response = self.client.get(
            "/api/v1/questions")
        self.assertEqual(response.status_code, 200)
