# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("./blueprint_module"))
from blueprint_module import auth_server_blueprint
from flask import Flask
from flask_cors import CORS

auth_server = Flask(__name__)
auth_server.config.from_object(__name__)
CORS(auth_server, resources={r"/api/v1/*": {"origins": "*"}})
auth_server.register_blueprint(auth_server_blueprint)


if __name__ == "__main__":
    auth_server.run(debug=True, port=15555)
