# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
from . import index_blueprint

from ..util import request_wants_json

@index_blueprint.app_errorhandler(400)
def bad_request(e):
    if request_wants_json():
        response = jsonify({'error': 'bad request'})
        response.status_code = 400
        return response
    return render_template('400.html'), 400

@index_blueprint.app_errorhandler(403)
def forbidden(e):
    if request_wants_json():
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403

@index_blueprint.app_errorhandler(404)
def page_not_found(e):
    if request_wants_json():
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404

@index_blueprint.app_errorhandler(500)
@index_blueprint.app_errorhandler(Exception)
def internal_server_error(e):
    if request_wants_json():
        response = jsonify({
            'error' : 'internal server error',
            'str_e' : str(e),
            'repr_e': repr(e),
        })
        response.status_code = 500
        return response

    context = {
        'str_e' : str(e),
        'repr_e': repr(e),
    }
    return render_template('500.html', **context), 500
