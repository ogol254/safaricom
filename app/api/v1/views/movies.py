import re
import json
import string

# third party packages
from flask_restplus import Resource
from statistics import mean
from flask import jsonify, make_response, request, g
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.movies_models import MoviesModels
from ..models.comment_models import CommentModel
from ..utils.serializers import MovieDTO
from ..utils.auth_validation import auth_required

api = MovieDTO().api
new_movie = MovieDTO().n_movie
new_movie_resp = MovieDTO().n_movie_resp
all_movies = MovieDTO().all_movie
all_movies_resp = MovieDTO.all_movies_resp
comment_resp = MovieDTO.n_comment_ns


def _validate_movie(record):
    """This function validates the user input and rejects or accepts it"""
    for key, value in record.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))


@api.route("/")
class Movies(Resource):
    """This class collects the methods for the movies method"""

    docu_string = "This endpoint accepts POST requests to report an record"

    @api.doc(docu_string)
    @api.expect(new_movie, validate=True)
    @api.marshal_with(new_movie_resp, code=201)
    @auth_required
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            title = body['title']
            description = body['description'].strip()
            type = body['type'].strip()
            recommendation = body['recommendation'].strip()
            rating = body['rating']

        except (KeyError, IndexError) as e:
            raise BadRequest

        movie_data = {
            "title": title,
            "description": description,
            "flag": "unwatched",
            "type": type,
            "recommendation" : recommendation, 
            "rating" : rating
        }

        _validate_movie(movie_data)
        movie = MoviesModels(**movie_data)
        resp = movie.save()
        response = {
            "message": resp
        }

        return response, 201

    
    docu_string = "This endpoint allows to get list of all movies"
    @api.doc(docu_string)
    @api.marshal_with(all_movies_resp, code=200)
    @auth_required
    def get(self):
        resp = MoviesModels().get_all()
        movies_list = {
            "message": "Success",
            "movies": resp
        }

        return movies_list, 200

@api.route("/<string:flag>")
class MovieFlag(Resource):

    @api.marshal_with(all_movies_resp, code=200)
    @auth_required
    def get(self, flag):
        if flag == 'all':
            resp = MoviesModels().get_all()
        else:
            resp = MoviesModels().get_flag(flag)
        
        movies_list = {
            "message": "Success",
            "movies": resp
        }
        return movies_list, 200


@api.route('/<int:film_id>')
class GetSpecifiedMovie(Resource):
    """docstring for GetSpecifiedrecord"""

    docu_string = "This endpoint allows to get a specific movie"

    @api.doc(docu_string)
    @api.marshal_with(all_movies_resp, code=200)
    @auth_required
    def get(self, film_id):
        if MoviesModels().check_exists("films", "film_id", film_id) == False:
            raise NotFound("No such film in our records")

        film = MoviesModels().get_one(film_id)
        comments = CommentModel().get_specif_record_comments(film_id)
        if not comments:
            comments = "No comments exists"
        films = {
            "message": "film",
            "movies": film, 
            "comment":comments
        }

        return films, 200

    docu_string = "This endpoint allows to edit a specific movie"
    @api.marshal_with(new_movie_resp, code=201)
    def put(self, film_id):
        if MoviesModels().check_exists("films", "film_id", film_id) == False:
            raise NotFound("No such film in our records")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "films"
            MoviesModels().update_item(table=_table_name,
                                      field=field,
                                      data=value,
                                      item_field="film_id",
                                      item_id=int(film_id))

            resp = {
                "message": "{} updated to {}".format(field, value)
            }

        return resp, 200

    docu_string = "This endpoint allows to soft delete a specific movie"
    @api.marshal_with(new_movie_resp, code=201)
    @auth_required
    def delete(self, film_id):
        if MoviesModels().check_exists("films", "film_id", film_id) == False:
            raise NotFound("No such film in our records")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = {"archive": 1}

        for field, value in body.items():
            _table_name = "films"
            MoviesModels().update_item(table=_table_name,
                                      field=field,
                                      data=value,
                                      item_field="film_id",
                                      item_id=int(film_id))

            resp = {
                "message": "Deleted"
            }

        return resp, 200

@api.route('/<int:film_id>/watch')
class WatchMoview(Resource):
    """docstring for GetSpecifiedrecord"""

    docu_string = "This endpoint allows to edit a specific movie"
    @auth_required
    @api.marshal_with(new_movie_resp, code=201)
    def get(self, film_id):
        if MoviesModels().check_exists("films", "film_id", film_id) == False:
            raise NotFound("No such film in our records")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = {"flag": "watched"}

        for field, value in body.items():
            _table_name = "films"
            MoviesModels().update_item(table=_table_name,
                                      field=field,
                                      data=value,
                                      item_field="film_id",
                                      item_id=int(film_id))

            resp = {
                "message": "Watched"
            }

        return resp, 200


