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


class Testmovies(BaseTest):
    """This class collects all the test cases for the users"""

    def test_adding_a_movie(self):
        """Test adding a movie using a POST request"""
        movie = self.post_movie(self.movie)
        self.assertEqual(movie.status_code, 201)
        # self.assertEqual(movie.json['message'], "Success")

    def test_getting_all_movies(self):
        """Test that an admin user get all movies using a GET request"""
        post = self.post_movie(self.movie)
        login = self.login_user(data=self.user)
        token = login.json['AuthToken']
        get = self.get(path="movies", auth=token)
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['message'], "Success")

    def test_getting_single_movie_admin(self):
        """Test that an admin user get all movies using a GET request"""
        post = self.post_movie(self.movie)
        movie_id = post.json['message']
        path = "movies/{}".format(int(movie_id))
        login = self.login_user(data=self.user)
        token = login.json['AuthToken']
        get = self.get(path=path, auth=token)
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['message'], "film")

    def test_editing_movie_admin(self):
        """Test that an admin user get all movies using a PUT request"""
        post = self.post_movie(self.movie)
        movie_id = post.json['message']
        path = "movies/{}".format(int(movie_id))
        login = self.login_user(data=self.user)
        token = login.json['AuthToken']
        data = {"type": "series"}
        put = self.put(path=path, data=data, auth=token)
        self.assertEqual(put.status_code, 200)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()