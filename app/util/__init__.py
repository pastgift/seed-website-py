# -*- coding: utf-8 -*-

from functools import wraps
from flask import request, abort, g
from flask.ext.login import current_user

import uuid
import time
import hashlib
import random

try:
    import simplejson as json
except:
    import json

from .logger_helper import add_log
from .captcha_helper import gen_captcha

def acl_required(action):
    def acl_required_decorater(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.can(action):
                abort(403)

            return func(*args, **kwargs)
        return decorated_view
    return acl_required_decorater

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def fill_form(form, **keyword):
    for k, v in keyword.items():
        try:
            form.__getattribute__(k).data = v
        except:
            pass

def get_sha1(v):
    sha1 = hashlib.sha1()
    sha1.update(str(v))

    sha1_string = sha1.hexdigest()
    return sha1_string

def get_md5(s):
    md5 = hashlib.md5()
    md5.update(str(s))

    md5_string = md5.hexdigest()
    return md5_string

def get_rand_password(length=8):
    samples_group = [
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'abcdefghijklmnopqrstuvwxyz',
        '0123456789',
    ]

    rand_password = ''
    for i in xrange(length):
        samples = samples_group[i % 3]
        rand_index = random.randint(0, len(samples) - 1)
        rand_password += samples[rand_index]

    return rand_password

def get_rand_string(length=32):
    samples = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    rand_string = ''
    for i in xrange(length):
        rand_index = random.randint(0, len(samples) - 1)
        rand_string += samples[rand_index]

    return rand_string

class FakePagination(object):
    def __init__(self, page_num, page_info):
        self.page_info = page_info

        self.total    = page_info['totalRecords']
        self.has_prev = page_num > 1
        self.prev_num = page_num - 1
        self.page     = page_num
        self.has_next = page_num < page_info['totalPages']
        self.next_num = page_num + 1

        self.page_list = xrange(1, page_info['totalPages'] + 1)

    def iter_pages(self, *args, **kwargs):
        return self.page_list
