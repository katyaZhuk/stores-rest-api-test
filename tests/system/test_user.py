import json

from models.user import UserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "test", "password": "123456"})

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertEqual(json.loads(response.data), {'message': 'User created successfully'})

    # non-working test
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "test", "password": "123456"})
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '123456'
                }), headers={'Content-Type': 'application/json'})

                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "test", "password": "123456"})
                response = client.post("/register", data={"username": "test", "password": "123456"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists"},
                                     json.loads(response.data))
