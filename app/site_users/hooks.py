# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, flash
from flask.ext.login import current_user, login_required
from . import site_users_blueprint

from ..util import acl_required

@site_users_blueprint.before_request
@login_required
@acl_required('enterManageUsers')
def before_request():
    pass

