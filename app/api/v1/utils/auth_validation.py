"""
This module collects the utilities for authorization.
"""
from functools import wraps

from flask import request, g
from werkzeug.exceptions import BadRequest, Unauthorized

from ..models.base_model import BaseModel


def auth_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        """Checks the validity of the header and raises a corresponding error"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise BadRequest("This endpoint requires authorization")
        auth_token = auth_header.split(" ")[1]
        response = BaseModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            raise Unauthorized("You are not authorized to access this resource")
        else:
            g.user = response
            return func(*args, **kwargs)
    return wrap