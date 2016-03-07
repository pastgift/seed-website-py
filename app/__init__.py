# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.babel import Babel, gettext as _
from config import config

db        = SQLAlchemy()
bootstrap = Bootstrap()
moment    = Moment()
babel      = Babel()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'site_auth.login'
login_manager.login_message = _('Please login')
login_manager.login_message_category = 'danger'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .index import index_blueprint
    app.register_blueprint(index_blueprint)

    # Site Modules
    from .site_auth import site_auth_blueprint
    app.register_blueprint(site_auth_blueprint, url_prefix='/site_auth')

    from .site_users import site_users_blueprint
    app.register_blueprint(site_users_blueprint, url_prefix='/site_users')

    return app
