# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length, EqualTo
from wtforms import ValidationError
from flask.ext.babel import lazy_gettext as _
