# -*- coding: utf-8 -*-

from flask import Blueprint

site_users_blueprint = Blueprint('site_users', __name__)

from . import views, hooks
