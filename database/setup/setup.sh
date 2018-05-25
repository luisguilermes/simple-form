#!/bin/bash

echo ******************************************************
echo Iniciando Replica Set
echo ******************************************************

sleep 10
mongo mongodb://mongo1:27017 replicaSet.js