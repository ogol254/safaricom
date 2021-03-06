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


class BaseTest(unittest.TestCase):
    """docstring for BaseTest"""
    api_prefix = "/api/v1/"

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "first_name": "Abraham",
            "last_name": "Ogol",
            "email": "abramogosl@gmail.com",
            "password": "ogolpass"
        }

        self.movie = {
            "title": "Cage Masterr",
            "description" : "Watching movies is a good way to spend sod like to",
            "rating" : 5,
            "recommendation": "Highly",
            "type" : "Movie"
        }


        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_db()

    def endpoint_path(self, path):
        return "/api/v1/"+path

    def post(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=paths, data=dto, headers=headers, content_type='application/json')
        return res

    def get(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.get(path=paths, headers=headers, content_type='application/json')
        return res

    def put(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.put(path=paths, data=dto, headers=headers, content_type='application/json')
        return res

    def delete(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.delete(path=paths, headers=headers, content_type='application/json')
        return res

    def register(self):
        register = self.post(path="auth/signup", data=self.user, auth=None)
        return register  

    def login_user(self, data):
        register = self.register()
        login = self.post(path="auth/signin", data=data, auth=None)
        return login

    def post_movie(self, data):
        login = self.login_user(data=self.user)
        token = login.json['AuthToken']
        res = self.post(path="movies", data=data, auth=token)
        return res


    def get_headers(self, authtoken=None):
        headers = {
            "Authorization": "Bearer {}".format(authtoken),
            "content_type": 'application/json'
        }
        return headers