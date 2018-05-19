# -*- coding: utf-8 -*-

from flask import jsonify

from simpleform import app

@app.route("/api/v1/info", methods = ['GET'])
def home_index():
    api_list = [
        {
            'version'   : 'v1',
            'buildtime' : '2018-05-19',
            'links'     : '/api/v1/sugestoes',
            'methods'   : 'get, post, put, delete'
        }
    ]
    return jsonify({'api_version': api_list}), 200