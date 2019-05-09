from flask_restplus import Namespace, fields

class AuthDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    user = api.model('login request', {
        'email': fields.String(required=True, description="user's id number"),
        'password': fields.String(required=True, description="user's password")
    })
    user_resp = api.model('response to login', {
        'message': fields.String(required=True, description="success or fail message"),
        'AuthToken': fields.String(required=True, description="authentication token"),
        'email': fields.String(required=True, description="user's name")
    })
    validate_user_resp = api.model('validation request', {
        'message': fields.String(required=True, description="success message"),
        'email': fields.String(required=True, description="user id"),
        'name': fields.String(required=True, description="name")
    })
    n_user = api.model('new user request', {
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'email': fields.String(required=True, description="user's email"),
        'password': fields.String(required=True, description="user's password")
    })

class MovieDTO(object):
    """User Data Transfer Object"""
    api = Namespace('movie', description='Movies ')
    n_movie = api.model('new moview ost request', {
        'title': fields.String(required=True, description="title"),
        'description': fields.String(required=True, description="description"),
        'type': fields.String(required=True, description="type"),
        'recommendation': fields.String(required=True, description="recommendation"),
        'rating': fields.Integer(required=True, description="rating")
    })
    n_movie_resp = api.model('response to login', {
        'message': fields.String(required=True, description="success or fail message")
    })
    all_movie = api.model('all movies response', {
        'film_id': fields.String(required=True, description="film_id"),
        'title': fields.String(required=True, description="title"),
        'description': fields.String(required=True, description="description"),
        'flag': fields.String(required=True, description="flag"),
        'type': fields.String(required=True, description="type"),
        'recommendation': fields.String(required=True, description="recommendation"),
        'rating': fields.Integer(required=True, description="rating"),
        'created_on': fields.String(required=True, description="created_on")
    })
    n_comment_ns = api.model('Response for fetching a comment', {
        'comment_id': fields.Integer(required=True, description="comment id number"),
        'comment': fields.String(required=True, description="comment id number"),
        'rating': fields.Integer(required=True, description="rating "),
        'created_by': fields.String(required=True, description="who created the comemnt"),
        'created_on': fields.String(required=True, description="date")
    })
    all_movies_resp = api.model('Reesponse for adding all movies', {
        'message': fields.String(required=True, description="success message"),
        'movies': fields.List(fields.Nested(all_movie), required=True, description="list of all the questions"),
        # 'comment': fields.String(required=True, description="created_on")
        'comment': fields.List(fields.Nested(n_comment_ns), required=True, description="list of all the questions")
    })
    

class CommentDTO(object):
    """docstring for CommentDTO"""
    api = Namespace('comments', description='comemnts Proceses')
    n_comment = api.model('new comment post  request', {
        'comment': fields.String(required=True, description="description of the comment"),
        'rating': fields.Integer(required=True, description="rating")
    })
    n_comment_resp = api.model('Response for adding a new record', {
        'message': fields.String(required=True, description="success message"),
        'comment_id': fields.Integer(required=True, description="comment id number")
    })
