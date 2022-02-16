# -*- coding: utf-8 -*-
import atexit
import logging
import os
import pytz
import sys
sys.path.append(os.path.abspath("./blueprint_module"))
sys.path.append(os.path.abspath("../utils"))

from apscheduler.schedulers.background import BackgroundScheduler
from blueprint_module import auth_server_blueprint
from blueprint_module import clean_all_expired_auth_code_data
from flask import Flask
from flask.logging import default_handler
from flask_cors import CORS
from utils import RequestFormatter

auth_server = Flask(__name__)
auth_server.config.from_object(__name__)
auth_server.logger.setLevel(logging.INFO)
_RequestFormatter = RequestFormatter(
    "[%(asctime)s][%(levelname)s] %(remote_addr)s requested %(url)s - \n"
    "%(message)s"
)
default_handler.setFormatter(_RequestFormatter)
CORS(auth_server, resources={r"/api/v1/*": {"origins": "*"}})
auth_server.register_blueprint(auth_server_blueprint)

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Shanghai"))
scheduler.add_job(func=clean_all_expired_auth_code_data, trigger="interval", seconds=86400)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
