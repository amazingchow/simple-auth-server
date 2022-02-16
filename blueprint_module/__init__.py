# -*- coding: utf-8 -*-
from flask import Blueprint
auth_server_blueprint = Blueprint("auth_server_blueprint", __name__)

from . import del_auth_code
from . import keepalive
from . import new_auth_code
from . import verify_auth_code
from .cronjob import clean_all_expired_auth_code_data
__all__ = [
    auth_server_blueprint,
    clean_all_expired_auth_code_data,
]
