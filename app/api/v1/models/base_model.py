"""
This module defines the base model and associated functions
"""
from datetime import datetime, timedelta
import jwt
import os

from flask import jsonify, make_response

from ....db_config import init_db
from .... import create_app


class BaseModel(object):
    """
    This class encapsulates the functions of the base model
    that will be shared across all other models
    """

    def __init__(self):
        """initialize the database"""
        self.db = init_db()

    def update_item(self, table, field, data, item_field, item_id):
        """update the field of an item given the item_id"""

        dbconn = self.db
        curr = dbconn.cursor()
        updated = curr.execute("UPDATE {} SET {}='{}' \
                     WHERE {} = {} ;".format(table, field, data, item_field, item_id))
        dbconn.commit()
        if updated:
            return True

    def get_user_by_email(self, email):
        """return user from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT first_name, last_name, password, email\
            FROM users WHERE email='%s'""" % (email))
        data = curr.fetchone()
        curr.close()
        return data

    @staticmethod
    def encode_auth_token(email):
        """Function to generate Auth token
        """
        # import pdb;pdb.set_trace()
        APP = create_app()
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": email
            }
            token = jwt.encode(
                payload,
                APP.config.get('SECRET_KEY'),
                algorithm="HS256"
            )
            resp = token
        except Exception as e:
            resp = e

        return resp

    def blacklisted(self, token):
        dbconn = self.db
        curr = dbconn.cursor()
        query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
        curr.execute(query, [token])
        if curr.fetchone():
            return True
        return False

    def decode_auth_token(self, auth_token):
        """This function takes in an auth
        token and decodes it
        """
        APP = create_app()
        if self.blacklisted(auth_token):
            return "Token has been blacklisted"
        secret = APP.config.get('SECRET_KEY')
        try:
            payload = jwt.decode(auth_token, secret)
            return payload['sub']  # user id
        except jwt.ExpiredSignatureError:
            return "The token has expired"
        except jwt.InvalidTokenError:
            return "The token is invalid"

    def check_exists(self, table, field, data):
        """Check if the records exist"""
        curr = self.db.cursor()
        query = "SELECT * FROM {} WHERE {}='{}'".format(table, field, data)
        curr.execute(query)
        data = curr.fetchone()
        if not data:
            return False
        return True

    def _type(self):
        """returns the name of the inheriting class"""
        return self.__class__.__name__

    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass
