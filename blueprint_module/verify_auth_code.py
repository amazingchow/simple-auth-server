# -*- coding: utf-8 -*-
import datetime
import os
import sys
sys.path.append(os.path.abspath("../concurrency_safe_shelve"))
sys.path.append(os.path.abspath("../utils"))

from . import auth_server_blueprint
from .constant import _auth_code_db_name
from concurrency_safe_shelve import open_thread_safe_shelf
from flask import request
from flask import Response
from flask_api import status as StatusCode
from utils import gen_auth_code_hash


# 验证激活码接口
@auth_server_blueprint.route("/api/v1/authcode/verify", methods=["GET", "HEAD"])
def verify_auth_code():
    auth_code = request.args.get("authcode", "")
    if len(auth_code) != 6:
        return Response(
            "Invalid auth_code",
            status=StatusCode.HTTP_400_BAD_REQUEST,
        )

    with open_thread_safe_shelf("./{}".format(_auth_code_db_name), flag="r") as db:
        if auth_code not in db.keys():
            return Response(
                "Invalid auth_code",
                status=StatusCode.HTTP_400_BAD_REQUEST,
            )

        salt = db[auth_code]["salt"]
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        auth_code_hash = gen_auth_code_hash(auth_code, salt, today)
        auth_code_hash_list = db[auth_code]["hash_list"]
        if auth_code_hash not in auth_code_hash_list:
            return Response(
                "Invalid auth_code",
                status=StatusCode.HTTP_400_BAD_REQUEST,
            )

    return Response(
        "Valid auth_code",
        status=StatusCode.HTTP_200_OK,
    )
