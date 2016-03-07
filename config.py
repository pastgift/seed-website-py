# -*- coding: utf-8 -*-

import os
import yaml
basedir = os.path.abspath(os.path.dirname(__file__))

# Load ACL Action file
_ACL_ACTIONS = None
with open(basedir + '/acl-actions.yaml') as _f:
    _ACL_ACTIONS = yaml.load(_f.read())

class Config(object):
    ADMIN_EMAIL                    = os.environ.get('ADMIN_EMAIL')
    SECRET_KEY                     = os.environ.get('SECRET_KEY') or 'h3bF9paWv9nNfAEo'
    SSL_DISABLE                    = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN  = True
    SQLALCHEMY_RECORD_QUERIES      = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BOOTSTRAP_SERVE_LOCAL          = True
    RECORDS_PER_PAGE               = 15
    FLASKY_SLOW_DB_QUERY_TIME      = 0.5
    BABEL_DEFAULT_LOCALE           = 'en'

    ACL_ACTIONS               = _ACL_ACTIONS['aclActions']
    ADMIN_DEFAULT_ACL_ACTIONS = _ACL_ACTIONS['adminDefaultAclActions']
    LIMITED_ACL_ACTIONS       = _ACL_ACTIONS['limitedAclActions']

    @classmethod
    def init_app(cls, app):
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        print 'Admin Email is ', app.config.get('ADMIN_EMAIL')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')

config = {
    'development': DevelopmentConfig,
    'production' : ProductionConfig,

    'default': DevelopmentConfig
}
