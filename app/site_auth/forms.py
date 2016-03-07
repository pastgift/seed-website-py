# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import session
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from flask.ext.babel import lazy_gettext as _

from ..models import User

class LoginForm(Form):
    email = StringField(validators=[
            Required(message=_('Please enter your email')),
            Length(1, 64),
            Email(message=_('Please enter a correct email'))])

    password = PasswordField(validators=[
            Required(message=_('Please enter your password'))])

    captcha = StringField(validators=[
            Length(4, message=_('Please enter a 4-length CAPTCHA code')),
            Required(message=_('Please enter the CAPTCHA code'))])

    keep_login = BooleanField(default=True)

    submit = SubmitField(_('Login'))

    def validate_email(self, field):
        field.data = field.data.strip()

        if not self.password.data:
            return

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            raise ValidationError(_('Wrong email or password'))

        if not user.is_active:
            raise ValidationError(_('Your account has been disabled'))

    def validate_password(self, field):
        if not self.email.data:
            return

        user = User.query.filter_by(email=self.email.data).first()
        if (user is None) or (not user.verify_password(field.data)):
            raise ValidationError(_('Wrong email or password'))

    def validate_captcha(self, field):
        field.data = field.data.strip()

        if session['login_captcha'].lower() != field.data.lower():
            field.data = ''
            raise ValidationError(_('Wrong CAPTCHA code'))

class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[
            Required(message=_('Please enter the old password'))])

    password = PasswordField(validators=[
            Required(message=_('Please enter the new password')),
            EqualTo('password2', message=_('The new passwords you entered do not match'))])

    password2 = PasswordField(validators=[
            Required(message=_('Please confirm new password'))])

    submit = SubmitField(_('Change Password'))
