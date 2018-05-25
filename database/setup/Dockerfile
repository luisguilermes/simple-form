FROM mongo:3.4

WORKDIR /usr/src/configs

COPY replicaSet.js .
COPY setup.sh .

CMD ["./setup.sh"]