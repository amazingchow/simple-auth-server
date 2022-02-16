# -*- coding: utf-8 -*-
import datetime
import hashlib
import random
import re


def gen_auth_code():
    auth_code_nums = [str(random.randrange(10)) for _ in range(6)]
    return "".join(auth_code_nums)


def gen_salt():
    salt_nums = [str(random.randrange(10)) for _ in range(8)]
    return "".join(salt_nums)


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


ALL_DIGIT_NUMS_AND_LETTERS = [str(i) for i in range(0, 10)] + \
    [str(chr(i)) for i in range(ord('a'), ord('z') + 1)] + \
    [str(chr(i)) for i in range(ord('A'), ord('Z') + 1)]
ALL_DIGIT_NUMS_AND_LETTERS_TOTAL = len(ALL_DIGIT_NUMS_AND_LETTERS)


def gen_n_digit_nums_and_letters(n: int):
    for i in range(len(ALL_DIGIT_NUMS_AND_LETTERS) - 1, 0, -1):
        j = random.randrange(i + 1)
        ALL_DIGIT_NUMS_AND_LETTERS[i], ALL_DIGIT_NUMS_AND_LETTERS[j] = ALL_DIGIT_NUMS_AND_LETTERS[j], ALL_DIGIT_NUMS_AND_LETTERS[i]
    nums_and_letters = [ALL_DIGIT_NUMS_AND_LETTERS[random.randrange(ALL_DIGIT_NUMS_AND_LETTERS_TOTAL)] for _ in range(n)]
    return "".join(nums_and_letters)
