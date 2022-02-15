# -*- coding: utf-8 -*-
from . import auth_server_blueprint
from flask import jsonify


# 探活接口
@auth_server_blueprint.route("/api/v1/keepalive", methods=["GET"])
def keepalive():
    return jsonify("OK")
