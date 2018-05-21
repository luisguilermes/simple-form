# -*- coding: utf-8 -*-
from pymongo import MongoClient

DB_NAME = 'simpleform_db'
COLLECTION_NAME = 'sugestoes'
MONGO_URI = "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=simpleformrs"


class ConnectionFactory:

    def __init__(self):
            self.connection = MongoClient(MONGO_URI)

    def get_connection(self):
        if(self.create_mongodatabase() == 0):
            return self.connection.simpleform_db
        else:
            return None

    # Initialize Database
    def create_mongodatabase(self):
        try:
            dbnames = self.connection.database_names()
            if DB_NAME not in dbnames:
                db = self.connection.simpleform_db.sugestoes

                db.insert({
                    "nome": "teste",
                    "email": "teste@gmail.com",
                    "sugestao": "Testes"
                })

                print("Database Initialize completed!")
            else:
                print("Database already Initialized!")
            return 0
        except:
            return 1