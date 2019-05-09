"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from contextlib import closing
from random import choice, randint

# local imports
from .. import create_app
from ..db_config import destroy_db, init_db

from .base_tests import BaseTest


class TestAuth(unittest.TestCase):
    """This class collects all the test cases for the users"""
    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "first_name": "Abraham",
            "last_name": "Ogol",
            "email": "abramogol@gmails.com",
            "password": "ogolpass"
        }


        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_db()

    def register(self):
        res = self.client.post(path="/api/v1/auth/signup", data=json.dumps(self.user), content_type='application/json')
        return res
    
    def login(self):
        reg = self.register()
        res = self.client.post(path="/api/v1/auth/signup", data=json.dumps(self.user), content_type='application/json')
        return res

    def test_user_signup(self):
        """Test that a user can signup using a POST request"""
        reg = self.register()
        self.assertEqual(reg.status_code, 201)

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        reg = self.register()
        login = self.login_user()
        self.assertEqual(login.json['message'], "Success")
        self.assertEqual(login.status_code, 200)

    def test_user_logout(self):
        """Test that the user can logout using a POST request"""
        reg = self.register()
        login = self.login_user()
        token = login.json['AuthToken']
        logout = self.post(path="/api/v1/auth/signout", data=self.user_admin, auth=token)
        self.assertEqual(logout.status_code, 200)

    def test_invalid_data(self):
        """Test that an unregistered user cannot log in"""
        # generate random username and password
        un_user = {
            "password": "".join(choice(
                                string.ascii_letters) for x in range(randint(7, 10))),
            "email": "".join(choice(
                string.ascii_letters) for x in range(randint(7, 10))),
        }
        # attempt to log in
        login = self.post(path="/api/v1/auth/signin", data=un_user, auth=None)
        self.assertEqual(login.status_code, 400)

    def test_an_unregistered_user(self):
        """Test that an unregistered user cannot log in"""
        data = {
            "email": "ajj@hh.com",
            "password": "badadmnsn"
        }
        path = 'auth/signin'
        login = self.post(path="/api/v1/auth/signin", data=data, auth=None)
        self.assertEqual(login.status_code, 401)
        self.assertEqual(login.json['message'], "Your details were not found, please sign up")

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()