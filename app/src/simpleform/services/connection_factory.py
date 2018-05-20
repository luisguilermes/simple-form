# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient

DB_NAME = 'simpleform_db'
COLLECTION_NAME = 'sugestoes'
MONGO1=os.environ.get("MONGO1")
MONGO2=os.environ.get("MONGO2")
MONGO3=os.environ.get("MONGO3")
REPLICA_SET='simpleformrs'
MONGO_URI="mongodb://{}:27017,{}:27017,{}:27017/?replicaSet={}".format(MONGO1, MONGO2, MONGO3, REPLICA_SET)

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
                    "nome": "Yuri Carlos Diogo das Neves",
                    "email": 13,
                    "sugestao": 9
                })

                print("Database Initialize completed!")
            else:
                print("Database already Initialized!")
            return 0
        except:
            return 1
