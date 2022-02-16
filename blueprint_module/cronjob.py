# -*- coding: utf-8 -*-
import datetime
import os
import sys
sys.path.append(os.path.abspath("../concurrency_safe_shelve"))
sys.path.append(os.path.abspath("../utils"))

from .constant import _auth_code_db_name
from concurrency_safe_shelve import open_thread_safe_shelf
from utils import common_logger
from utils import gen_auth_code_hash


def clean_all_expired_auth_code_data():
    with open_thread_safe_shelf("./{}".format(_auth_code_db_name), flag="c", writeback=True) as db:
        auth_code_list = db.keys()
        for auth_code in auth_code_list:
            salt = db[auth_code]["salt"]
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            auth_code_hash = gen_auth_code_hash(auth_code, salt, today)
            auth_code_hash_list = db[auth_code]["hash_list"]
            if auth_code_hash not in auth_code_hash_list:
                del db[auth_code]
                common_logger.info("auth code <{}> is stale, we do remove it".format(auth_code))
        db.sync()
        common_logger.info("do daily job to clean all expired auth code data")
