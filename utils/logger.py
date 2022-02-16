# -*- coding: utf-8 -*-
import logging

common_logger = logging.getLogger("auth_server_common_logger")
common_logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler("./auth_server_common.log", "w")
__FileHandler.setFormatter(__Formatter)
common_logger.addHandler(__FileHandler)
