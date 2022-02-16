# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("../concurrency_safe_shelve"))
sys.path.append(os.path.abspath("../utils"))

from . import auth_server_blueprint
from .constant import _auth_code_db_name
from concurrency_safe_shelve import open_thread_safe_shelf
from flask import current_app
from flask import request
from flask import Response
from flask_api import status as StatusCode


# 删除激活码接口
@auth_server_blueprint.route("/api/v1/authcode", methods=["DELETE"])
def del_auth_code():
    auth_code = request.args.get("authcode", "")
    if len(auth_code) != 6:
        current_app.logger.error("invalid auth_code: {}".format(auth_code))
        return Response(
            "Invalid auth_code",
            status=StatusCode.HTTP_400_BAD_REQUEST,
        )

    with open_thread_safe_shelf("./{}".format(_auth_code_db_name), flag="w", writeback=True) as db:
        if auth_code not in db.keys():
            current_app.logger.error("not found auth_code: {}".format(auth_code))
            return Response(
                "Not found auth_code",
                status=StatusCode.HTTP_200_OK,
            )

        del db[auth_code]
        db.sync()
        current_app.logger.info("delete auth_code: {}".format(auth_code))

    return Response(
        "Delete auth_code",
        status=StatusCode.HTTP_200_OK,
    )
