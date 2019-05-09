"""
This module sets up the users resource
Authored by: Ogol
"""
from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import NotFound

version_one = Blueprint('version1', __name__, url_prefix="/api/v1")

from .views.auth import api as auth_ns
from .views.movies import api as movies
from .views.commentrate import api as cm_ns


api = Api(version_one,
          title='Movies  API',
          version='1.0',
          description="Safaricom Hackerthon")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(movies, path="/movies")
api.add_namespace(cm_ns, path="/movies/<int:film_id>/comment")