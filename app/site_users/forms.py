# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from flask.ext.babel import lazy_gettext as _

from ..models import User

class SearchUserForm(Form):
    email  = StringField()
    name   = StringField()
    submit = SubmitField(_('Search'))

class AddUserForm(Form):
    email = StringField(validators=[
            Required(message=_('Please enter a user email')),
            Length(1, 64),
            Email(message=_('Please enter a correct user email'))])

    name = StringField(validators=[
            Required(message=_('Please enter a user name')),
            Length(1, 64, message=_('Please enter a user name between 1 and 64 characters long'))])

    password = PasswordField(validators=[
            Required(message=_('Please enter a password')),
            EqualTo('password2', message=_('The passwords you entered do not match'))])

    password2 = PasswordField(validators=[
            Required(message=_('Please confirm the password'))])

    submit = SubmitField(_('Add'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email already existed'))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This name already existed'))

class EditUserForm(Form):
    email = StringField(validators=[
            Required(message=_('Please enter a user email')),
            Length(1, 64),
            Email(message=_('Please enter a correct user email'))])

    name = StringField(validators=[
            Required(message=_('Please enter a user name')),
            Length(1, 64, message=_('Please enter a user name between 1 and 64 characters long'))])

    password = PasswordField()

    submit = SubmitField(_('Edit'))

    def validate_email(self, field):
        if field.data != self.prev.email and \
                User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email already existed'))

class AclSettingForm(Form):
    acl_actions = TextAreaField()
    submit = SubmitField(_('OK'))

class SearchOperationRecordForm(Form):
    name           = StringField()
    email          = StringField()
    operation_note = StringField()

    submit = SubmitField(_('Search'))
