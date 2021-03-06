# -*- coding: utf-8 -*-
from flask import jsonify
from flask import abort

class SugestaoDao:

    def __init__(self, connection):
        self.connection = connection
        self.db = self.connection.sugestoes

    def lista_sugestoes(self):
        api_list = []
        for row in self.db.find():
            api_list.append(str(row))
            # print (api_list)
        return api_list

    def add_sugestao(self, nova_sugestao):
        api_list = []
        sugestoes = self.db.find({"email": nova_sugestao.email})
        for i in sugestoes:
            api_list.append(str(i))
        if api_list == []:
            self.db.insert(
                {
                "nome": nova_sugestao.nome,
                "email": nova_sugestao.email,
                "sugestao": nova_sugestao.sugestao
             })
            return "Success"
        else:
            abort(409)