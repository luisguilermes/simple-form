# -*- coding: utf-8 -*-

from flask import request, jsonify, make_response, abort
import socket

from simpleform import app
from ..services.connection_factory import ConnectionFactory
from ..dao.sugestao_dao import SugestaoDao
from ..models.sugestao import Sugestao

cf = ConnectionFactory()
connection = cf.get_connection()
if connection is None:
    exit(1)


@app.route("/api/v1/info", methods = ['GET'])
def home_index():
    api_list = [
        {
            'version'   : 'v1',
            'buildtime' : '2018-05-19',
            'links'     : '/api/v1/sugestoes',
            'methods'   : 'get, post, put, delete',
            'host'      : socket.gethostname()
        }
    ]
    return jsonify({'api_version': api_list}), 200

@app.route('/api/v1/sugestoes', methods = ['GET'])
def get_alunos():
    #return SugestaoDao(connection).lista_sugestoes()
    pass


@app.route('/api/v1/sugestoes', methods=['POST'])
def create_sugestao():
    if not request.json or not 'nome' in request.json or not 'email' in request.json or not 'sugestao' in request.json:
        abort(400)
    nova_sugestao = Sugestao(
        request.json['nome'],
        request.json['email'],
        request.json['sugestao'])
    result = SugestaoDao(connection).add_aluno(nova_sugestao)
    return jsonify({'status': result}), 201
