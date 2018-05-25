FROM python:2

WORKDIR /usr/src/app

RUN pip install --no-cache-dir zabbix-api==0.5.3

COPY setup.sh ./
COPY setup.py ./
CMD [ "./setup.sh" ]