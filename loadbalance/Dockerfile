FROM nginx

RUN apt-get update && \
    apt-get install -y zabbix-agent curl
COPY zabbix/zabbix_agentd.conf /etc/zabbix/
COPY zabbix/check_backend.sh /

COPY default.conf /etc/nginx/conf.d/default.conf
COPY ./template /usr/share/nginx/html
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]