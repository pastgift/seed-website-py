# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import render_template, abort, redirect, current_app, request, url_for, flash, make_response, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.babel import gettext as _

from . import site_auth_blueprint

from .forms import LoginForm, ChangePasswordForm
from .. import db
from ..models import User
from ..util import add_log, gen_captcha

from StringIO import StringIO

@site_auth_blueprint.route('/login_captcha', methods=['GET'])
def login_captcha():
    captcha_code, img = gen_captcha()
    session['login_captcha'] = captcha_code

    memory_stream = StringIO()
    img.save(memory_stream, 'GIF')

    output_resp = make_response(memory_stream.getvalue())
    output_resp.headers['Content-Type'] = 'image/gif'
    return output_resp

@site_auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'admin_email': current_app.config['ADMIN_EMAIL'].split('@'),
        'form'       : form,
    }

    # Open Page
    if not form.validate_on_submit():
        return render_template('site_auth/login.html', **context)

    # Submit
    user = User.query.filter_by(email=form.email.data).first()
    login_user(user, form.keep_login.data)

    if user:
        add_log('[Site User][Login] Login', user.id)
    return redirect(request.args.get('next') or url_for('index.index'))

@site_auth_blueprint.route('/logout')
@login_required
def logout():
    add_log('[Site User] Logged out')

    logout_user()
    flash(_('Logged out'), 'info')
    return redirect(url_for('index.index'))

@site_auth_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    context = {
        'form': form,
    }

    # Open Page
    if not form.validate_on_submit():
        return render_template('site_auth/change_password.html', **context)

    # Submit
    if current_user.verify_password(form.old_password.data):
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()

        flash(_('Password Changed'), 'success')

        add_log('[Site User][Change Password] Changed password')
        return redirect(url_for('index.index'))

    else:
        flash(_('Wrong old password'), 'danger')

        add_log('[Site User][Change Password] Try to change password but entered wrong old password')
        return redirect(url_for('site_auth.change_password'))

