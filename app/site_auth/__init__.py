# -*- coding: utf-8 -*-

from flask import Blueprint

site_auth_blueprint = Blueprint('site_auth', __name__)

from . import views
