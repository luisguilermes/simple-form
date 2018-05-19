FROM python:3.6

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==0.10.1 uWSGI==2.0.8

WORKDIR /app
COPY src /app
COPY run.sh /
EXPOSE 9090 9191
USER uwsgi

CMD ["/run.sh"]