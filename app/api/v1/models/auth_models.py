from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AuthModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, first_name="",  last_name="", email="", password="pass"):
        """initialize the user model"""
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.db = init_db()

    def save(self):
        """Add user details to the database"""
        user = {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password
        }
        # check if user exists
        if BaseModel().check_exists(table="users", field="email", data=user['email']):
            return False

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (first_name, last_name, email, password) \
            VALUES ( %(first_name)s, %(last_name)s,\
            %(email)s, %(password)s) RETURNING email;
            """
        curr.execute(query, user)
        email = curr.fetchone()[0]
        database.commit()
        curr.close()
        return email

    def logout_user(self, token):
        """This function logs out a user by adding thei token to the blacklist table"""
        conn = self.db
        curr = conn.cursor()
        query = """
                INSERT INTO blacklist 
                VALUES (%(tokens)s) RETURNING tokens;
                """
        inputs = {"tokens": token}
        curr.execute(query, inputs)
        blacklisted_token = curr.fetchone()[0]
        conn.commit()
        curr.close()
        return blacklisted_token
