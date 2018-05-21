FROM python:3.6

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app
COPY src /app
COPY run.sh /
EXPOSE 9090 9191
USER uwsgi

CMD ["/run.sh"]