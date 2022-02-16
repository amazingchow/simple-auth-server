# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("../concurrency_safe_shelve"))
sys.path.append(os.path.abspath("../utils"))

from . import auth_server_blueprint
from .constant import _access_token
from .constant import _auth_code_db_name
from concurrency_safe_shelve import open_thread_safe_shelf
from flask import current_app
from flask import jsonify
from flask import request
from flask import Response
from flask_api import status as StatusCode


# 返回所有激活码接口
@auth_server_blueprint.route("/api/v1/authcode", methods=["GET"])
def list_auth_code():
    access_token = request.headers.get("x-auth-token", "")
    if len(access_token) != 10 or access_token != _access_token:
        return Response(
            "Invalid x-auth-token",
            status=StatusCode.HTTP_401_UNAUTHORIZED,
        )

    auth_code_list = []
    with open_thread_safe_shelf("./{}".format(_auth_code_db_name), flag="r") as db:
        auth_code_list = [
            {
                "auth_code": auth_code,
                "user_email": db[auth_code]["user_email"],
                "expired_date": db[auth_code]["expired_date"],
            } for auth_code in db.keys()
        ]

    response_object = {
        "auth_code_count": len(auth_code_list),
        "auth_code_list": auth_code_list,
    }
    current_app.logger.info("return {} auth code".format(len(auth_code_list)))
    return jsonify(response_object)
