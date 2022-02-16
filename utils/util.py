# -*- coding: utf-8 -*-
import datetime
import hashlib
import random
import re


def gen_auth_code():
    auth_code_num = [str(random.randrange(10)) for _ in range(6)]
    return "".join(auth_code_num)


def gen_salt():
    salt_num = [str(random.randrange(10)) for _ in range(8)]
    return "".join(salt_num)


def gen_datetime_range(st_date_str: str, ed_date_str: str):
    st_date = datetime.datetime.fromisoformat(st_date_str)
    ed_date = datetime.datetime.fromisoformat(ed_date_str)
    span = ed_date - st_date
    for i in range(span.days + 1):
        yield (st_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")


def gen_auth_code_hash(auth_code: str, salt: str, email: str, date: str):
    h = hashlib.new("sha256")
    h.update(bytes("{}_{}_{}_{}".format(auth_code, salt, email, date), encoding="utf-8"))
    return h.hexdigest()


def validate_date_format(date: str):
    is_valid = True
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        is_valid = False
    finally:
        return is_valid


EMAIL_REGEX = re.compile(r"[^@|\s]+@[^@]+\.[^@|\s]+")

def validate_email_format(email: str):
    is_valid = True
    if EMAIL_REGEX.match(email) is None:
        is_valid = False
    return is_valid
