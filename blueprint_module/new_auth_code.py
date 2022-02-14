# -*- coding: utf-8 -*-
import datetime
import os
import sys
sys.path.append(os.path.abspath("../concurrency_safe_shelve"))
sys.path.append(os.path.abspath("../utils"))

from . import auth_server_blueprint
from .constant import _auth_code_db_name
from concurrency_safe_shelve import open_thread_safe_shelf
from flask import jsonify
from flask import request
from flask import Response
from flask_api import status as StatusCode
from utils import gen_auth_code
from utils import gen_auth_code_hash
from utils import gen_datetime_range
from utils import gen_salt
from utils import validate_date_format


# 生成激活码接口
@auth_server_blueprint.route("/api/v1/authcode/new", methods=["POST"])
def new_auth_code():
    payload = request.get_json()
    expired_date = payload.get("expired_date", "")
    if not validate_date_format(expired_date):
        return Response(
            "Invalid expired_date",
            status=StatusCode.HTTP_400_BAD_REQUEST,
        )

    auth_code = ""
    with open_thread_safe_shelf("./{}".format(_auth_code_db_name), flag="c") as db:
        while 1:
            auth_code = gen_auth_code()
            if auth_code not in db.keys():
                break

        salt = gen_salt()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        datetime_range = gen_datetime_range(today, expired_date)
        auth_code_hash_list = [gen_auth_code_hash(auth_code, salt, date) for date in datetime_range]

        db[auth_code] = {
            "salt": salt,
            "hash_list": auth_code_hash_list,
        }

    response_object = {"auth_code": auth_code, "expired_date": expired_date}
    return jsonify(response_object)
