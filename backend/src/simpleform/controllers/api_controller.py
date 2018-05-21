# -*- coding: utf-8 -*-
import json
from sys import exit
from flask import request, jsonify, make_response, abort
import socket

from simpleform import app
from ..services.connection_factory import ConnectionFactory
from ..dao.sugestao_dao import SugestaoDao
from ..models.sugestao import Sugestao

cf = ConnectionFactory()
connection = cf.get_connection()
if connection is None:
    exit(10)


@app.route("/v1/info", methods = ['GET'])
def home_index():
    api_list = [
        {
            'version'   : 'v1',
            'buildtime' : '2018-05-19',
            'links'     : '/api/v1/sugestoes',
            'methods'   : 'get, post',
            'host'      : socket.gethostname()
        }
    ]
    return jsonify({'api_version': api_list}), 200

@app.route('/v1/sugestoes', methods = ['GET'])
def get_sugestoes():
    result = SugestaoDao(connection).lista_sugestoes()
    return jsonify({'lista_sugestoes': result}), 200


@app.route('/v1/sugestoes', methods=['POST'])
def create_sugestao():
    json_data = json.loads(request.data)

    print(json_data)
    nova_sugestao = Sugestao(
        json_data['nome'],
        json_data['email'],
        json_data['sugestao'])
    result = SugestaoDao(connection).add_sugestao(nova_sugestao)
    return jsonify({'status': result}), 201



@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)


@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        print(request.data)
        return "JSON Message: " + json.dumps(request.json)

    else:
        return "415 Unsupported Media Type"