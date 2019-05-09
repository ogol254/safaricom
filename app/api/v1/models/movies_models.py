from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class MoviesModels(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, title='', description='', recommendation='', rating='', flag='', type=''):
        """initialize the user model"""
        self.title = title
        self.description = description
        self.recommendation = recommendation
        self.rating = rating
        self.flag = flag
        self.type = type
        self.db = init_db()

    def save(self):
        """Add fil details to the database"""
        movie = {
            "title": self.title,
            "description": self.description,
            "flag": self.flag,
            "type": self.type,
            "recommendation" : self.recommendation, 
            "rating" : self.rating
        }
        # check if movie exists
        if BaseModel().check_exists(table="films", field="title", data=movie['title']):
            return "Movie already exists"

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO films (title, description, flag, type, recommendation, rating) \
            VALUES ( %(title)s, %(description)s,%(flag)s, %(type)s, \
            %(recommendation)s, %(rating)s) RETURNING film_id;
            """
        curr.execute(query, movie)
        film_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return film_id

    def get_all(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT film_id, title, description, flag, type, recommendation, rating, 
            created_on FROM films WHERE archive=0 ORDER BY film_id DESC;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            film_id, title, description, flag, type, recommendation, rating, created_on = items
            movies = dict(
                film_id=int(film_id),
                title=title,
                description=description,
                flag=flag,
                type=type,
                recommendation=recommendation,
                rating=int(rating),
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(movies)
        return resp

    def get_one(self, fid):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT film_id, title, description, flag, type, recommendation, rating, 
            created_on FROM films WHERE archive=0 AND film_id=%s ORDER BY film_id DESC;"""
        curr.execute(query, [fid])
        ddata = curr.fetchone()
        resp = []
        curr.close()
        film_id, title, description, flag, type, recommendation, rating, created_on = ddata
        movie = dict(
            film_id=int(film_id),
            title=title,
            description=description,
            flag=flag,
            type=type,
            recommendation=recommendation,
            rating=int(rating),
            created_on=created_on.strftime("%B %d, %Y")
        )
        resp.append(movie)
        return resp

    def get_flag(self, flag):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT film_id, title, description, flag, type, recommendation, rating, 
            created_on FROM films WHERE archive=0 AND flag=%s ORDER BY film_id DESC;"""

        curr.execute(query, [flag])
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            film_id, title, description, flag, type, recommendation, rating, created_on = items
            movies = dict(
                film_id=int(film_id),
                title=title,
                description=description,
                flag=flag,
                type=type,
                recommendation=recommendation,
                rating=int(rating),
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(movies)
        return resp

   