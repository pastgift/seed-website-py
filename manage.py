# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

basedir = os.path.abspath(os.path.dirname(__file__))
ADDITIONAL_PACKAGE_PATH = [
    # Add lib path here
]
for p in ADDITIONAL_PACKAGE_PATH:
    package_abs_path = basedir + p
    if package_abs_path not in sys.path:
        sys.path.append(package_abs_path)

from app import create_app, db
from app.models import User, UserAcl, OperationRecord

from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    context = {
        'app': app,
        'db' : db,

        'User'           : User,
        'UserAcl'        : UserAcl,
        'OperationRecord': OperationRecord,
    }
    return context

@manager.command
def initdb():
    db.drop_all()
    db.create_all()

    admin_user = User.new(
        email=app.config.get('ADMIN_EMAIL'),
        password='admin!',
        name=u'admin')
    db.session.add(admin_user)
    db.session.commit()

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    if not app.config.get('ADMIN_EMAIL'):
        print 'Please set an env for `ADMIN_EMAIL`'
        sys.exit(1)

    manager.run()
