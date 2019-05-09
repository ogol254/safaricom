from datetime import datetime, timedelta

# local imports
from ....db_config import init_db
from .base_model import BaseModel


class CommentModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, created_by="", rating="", comment="text", movie_id=0):
        """initialize the user model"""
        self.comment = comment
        self.created_by = created_by
        self.movie_id = movie_id
        self.rating = rating
        self.db = init_db()

    def save_comment(self):
        """Add the comment details to the database"""
        comment = {
            "comment": self.comment,
            "created_by": self.created_by,
            "movie_id": self.movie_id,
            "rating" : self.rating
        }

        database = self.db
        curr = database.cursor()
        query = """INSERT INTO comentrate (comment, rating, created_by, movie_id) \
            VALUES (%(comment)s, %(rating)s, %(created_by)s, %(movie_id)s) RETURNING comment_id;
            """
        curr.execute(query, comment)
        comment_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(comment_id)

    def get_specif_record_comments(self, movie_id):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT comment_id, created_by, comment, rating, date_created FROM comentrate WHERE movie_id=%s ORDER BY date_created DESC;"""
        curr.execute(query, [movie_id])
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            comment_id, created_by, comment, rating, created_on = items

            comments = dict(
                comment_id=int(comment_id),
                comment=comment,
                rating=int(rating),
                created_by=created_by,
                created_on=created_on.strftime("%B %d, %Y")
            )
            resp.append(comments)

        return resp