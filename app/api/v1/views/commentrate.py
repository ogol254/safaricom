import re
import json
import string

# third party packages
from flask_restplus import Resource
from flask import jsonify, make_response, request, g
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.comment_models import CommentModel
from ..utils.serializers import CommentDTO
from ..utils.auth_validation import auth_required

api = CommentDTO().api
new_comment = CommentDTO().n_comment
new_comment_resp = CommentDTO().n_comment_resp



@api.route('/')
class Comments(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to comment"

    @api.doc(docu_string)
    @api.expect(new_comment, validate=True)
    @api.marshal_with(new_comment_resp, code=201)
    @auth_required
    def post(self, film_id):
        """This endpoint allows a logged in user to leave a comment and rating."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            comment = body['comment'].strip()
            rating = body['rating']

            if CommentModel().check_exists("films", "film_id", film_id) == False:
                raise BadRequest("This film does not exist")

        except (KeyError, IndexError) as e:
            raise BadRequest

        comment_data = {
            "movie_id": film_id,
            "created_by": g.user,
            "comment": comment,
            "rating": rating
        }

        comment = CommentModel(**comment_data)
        resp = comment.save_comment()

        response = {
            "message": "Success",
            "comment_id": resp
        }

        return response, 201

@api.route('/<int:comment_id>')
class GetSpecificComment(Resource):
    """docstring for GetSpecifiedcomment"""

    docu_string = "This endpoint edits a comment to a question"
    @api.marshal_with(new_comment_resp, code=200)
    @auth_required
    def put(self, movie_id, comment_id):
        if CommentModel().check_exists("comentrate", "comment_id", comment_id) == False:
            raise NotFound("No such comment in our comments")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "comments"
            CommentModel().update_item(table=_table_name,
                                       field=field,
                                       data=value,
                                       item_field="comment_id",
                                       item_id=int(comment_id))

            resp = {
                "message": "{} updated to {}".format(field, value),
                "comment_id": comment_id
            }

        return resp, 200