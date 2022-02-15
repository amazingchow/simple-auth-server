# -*- coding: utf-8 -*-
from flask import Blueprint
auth_server_blueprint = Blueprint("auth_server_blueprint", __name__)

from . import keepalive
from . import new_auth_code
from . import verify_auth_code
__all__ = [
    auth_server_blueprint,
]
