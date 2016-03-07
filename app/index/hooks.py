# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, flash, g
from flask.ext.login import current_user
from . import index_blueprint

from .. import db
from .. import babel
from ..models import User

from datetime import datetime

@index_blueprint.before_app_request
def before_request():
    if not request.user_agent.browser:
        return

    user_browser = request.user_agent.browser.lower()
    if user_browser != 'chrome':
        # Do some thing
        pass

@index_blueprint.after_app_request
def after_request(res):
    # Record latest access
    if current_user.is_authenticated:
        current_user.ping()

    return res

@babel.localeselector
def get_locale():
    '''
    Select Language Tag
    '''
    lang = request.cookies.get('lang', 'en')

    # Uncomment to auto match language
    # if not lang:
    #     lang = request.accept_languages.best_match(['zh_CN', 'zh_TW', 'ja'])

    babel_lang_alias = {
        'zh_CN': 'zh_Hans_CN',
        'zh_TW': 'zh_Hant_TW',
        'ja'   : 'ja_JP',
        # Add more languages
        #'<Setting Name>': 'Babel Locale Name'
    }

    datepicker_lang_alias = {
        'zh_CN': 'zh-CN',
        'zh_TW': 'zh-TW',
        # Add more languages
        #'<Setting Name>': 'jQuery-datapicker Locale Name'
    }

    g.lang            = lang
    g.babel_lang      = babel_lang_alias.get(lang, lang)
    g.datepicker_lang = datepicker_lang_alias.get(lang, lang)

    return g.babel_lang