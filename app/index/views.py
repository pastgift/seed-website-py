# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from . import index_blueprint

from ..util import add_log

@index_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')