# -*- coding: utf-8 -*-

import uuid
import hashlib
from datetime import datetime

from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.exceptions import ValidationError
from . import db, login_manager

class User(db.Model):
    __tablename__ = 'tb_users'
    id                = db.Column(db.String(64), primary_key=True)
    email             = db.Column(db.String(64), unique=True, index=True)
    password_hash     = db.Column(db.String(128))
    name              = db.Column(db.UnicodeText(64))
    status            = db.Column(db.String(64), default='normal')
    last_seen         = db.Column(db.DateTime())
    created_timestamp = db.Column(db.DateTime(), default=db.func.now())
    updated_timestamp = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def is_active(self):
        return self.status == 'normal'

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    @property
    def password(self):
        raise AttributeError('Can not get password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.email == current_app.config['ADMIN_EMAIL']

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self, action):
        if self.is_admin() and action in current_app.config['ADMIN_DEFAULT_ACL_ACTIONS']:
            return True

        if UserAcl.query.filter_by(user_id=self.id, action=action).first():
            return True

        return False

    def can_any(self, *actions):
        for action in actions:
            if self.can(action):
                return True
        else:
            return False

    def can_all(self, *actions):
        for action in actions:
            if not self.can(action):
                return False

        else:
            return True

    @staticmethod
    def new(**kwargs):
        kwargs['id'] = uuid.uuid4().hex
        return User(**kwargs)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.email

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def can(self, *args, **kwargs):
        return False

    can_any = can
    can_all = can

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class UserAcl(db.Model):
    __tablename__ = 'tb_user_acl'
    id                = db.Column(db.String(64), primary_key=True)
    user_id           = db.Column(db.String(64))
    action            = db.Column(db.String(128))
    created_timestamp = db.Column(db.DateTime(), default=db.func.now())
    updated_timestamp = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(UserAcl, self).__init__(**kwargs)

    @staticmethod
    def new(**kwargs):
        kwargs['id'] = uuid.uuid4().hex
        return UserAcl(**kwargs)

    def __repr__(self):
        return '<UserAcl %r, %r>' % (self.user_id, self.action)

class OperationRecord(db.Model):
    __tablename__ = 'tb_operation_records'
    id                = db.Column(db.String(64), primary_key=True)
    user_id           = db.Column(db.String(64))
    operation_note    = db.Column(db.Text())
    created_timestamp = db.Column(db.DateTime(), default=db.func.now())
    updated_timestamp = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        super(OperationRecord, self).__init__(**kwargs)

    @staticmethod
    def new(**kwargs):
        kwargs['id'] = uuid.uuid4().hex
        return OperationRecord(**kwargs)

    def __repr__(self):
        return '<OperationRecord %r>' % self.user_id
