#!/usr/bin/env bash

set -e

function mudar_env {
    env='docker-machine env '$1
    eval $($env)
}

# Cria maquinas
function cria_vm {

    if [ "$(docker-machine ls -q | grep $1)" = $1 ]; then
        docker-machine rm -y $1
        docker-machine create -d virtualbox $1
    else
        docker-machine create -d virtualbox $1
    fi

}

function criar_cluster_swarm {
    echo "CRIANDO MANAGER"
    cria_vm manager
    echo "CRIANDO WORKER1"
    sleep 5
    cria_vm worker1
    echo "CRIANDO WORKER2"
    sleep 5
    cria_vm worker2
    echo "PROMOVENDO CLUSTER SWARM"
    sleep 5
    promover_cluster
}

function promover_cluster {
    arg=''
    for server in manager worker1 worker2
    do
        if [ $server = 'manager' ]; then
            env='docker-machine env '$server
            eval $($env)
            arg=$(docker swarm init --advertise-addr eth1 | grep SWMTKN)
            echo $arg
        else
            env='docker-machine env '$server
            eval $($env)
            $arg
        fi
    done
}


function deploy_mongo {

    mudar_env manager
    docker network create --driver overlay --internal mongo
    docker node update --label-add mongo.replica=1 $(docker node ls -q -f name=manager)
    docker node update --label-add mongo.replica=2 $(docker node ls -q -f name=worker1)
    docker node update --label-add mongo.replica=3 $(docker node ls -q -f name=worker2)

    #cria volume manager
    mudar_env worker1
    docker volume create --name mongodata1
    docker volume create --name mongoconfig1

    #cria volume worker1
    mudar_env worker2
    docker volume create --name mongodata2
	docker volume create --name mongoconfig2


    #cria volume worker2
    docker volume create --name mongodata3
	docker volume create --name mongoconfig3

    #cria service
    mudar_env manager
    docker service create --replicas 1 --network mongo --mount type=volume,source=mongodata1,target=/data/db --mount type=volume,source=mongoconfig1,target=/data/configdb --constraint 'node.labels.mongo.replica == 1' --name mongo1 mongo:3.2 mongod --replSet simpleformrs
    docker service create --replicas 1 --network mongo --mount type=volume,source=mongodata2,target=/data/db --mount type=volume,source=mongoconfig2,target=/data/configdb --constraint 'node.labels.mongo.replica == 2' --name mongo2 mongo:3.2 mongod --replSet simpleformrs
    docker service create --replicas 1 --network mongo --mount type=volume,source=mongodata3,target=/data/db --mount type=volume,source=mongoconfig3,target=/data/configdb --constraint 'node.labels.mongo.replica == 3' --name mongo3 mongo:3.2 mongod --replSet simpleformrs

    echo "ESPERANDO MONGO SUBIR"
    sleep 300
    mudar_env manager
    docker exec -it $(docker ps -qf label=com.docker.swarm.service.name=mongo1) mongo --eval 'rs.initiate({ _id: "simpleformrs", members: [{ _id: 1, host: "mongo1:27017" }, { _id: 2, host: "mongo2:27017" }, { _id: 3, host: "mongo3:27017" }], settings: { getLastErrorDefaults: { w: "majority", wtimeout: 30000 }}})'
    docker exec -it $(docker ps -qf label=com.docker.swarm.service.name=mongo1) mongo --eval 'rs.status()'
    docker exec -it $(docker ps -qf label=com.docker.swarm.service.name=mongo1) mongo --eval 'rs.config()'
}

function main {
  echo "INICIANDO O DEPLOY"
  criar_cluster_swarm
  deploy_mongo
}

main