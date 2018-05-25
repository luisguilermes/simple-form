from zabbix_api import ZabbixAPI
import sys

zapi = ZabbixAPI(server="http://zabbix:80/")
zapi.login("Admin", "zabbix")


zapi.drule.create({
    "name": "Frontend Discovery",
    "iprange": sys.argv[1]+".1-255",
    "delay": "10",
    "dchecks": [{
        "type": "9",
        "key_": "is.frontend",
        "ports": "10050", "uniq": "0"
    }]})

zapi.drule.create({
    "name": "Backend Discovery",
    "iprange": sys.argv[1]+".1-255",
    "delay": "10",
    "dchecks": [{
        "type": "9",
        "key_": "is.backend",
        "ports": "10050", "uniq": "0"
    }]})

zapi.hostgroup.create({"name": "Backend Hosts"})
zapi.hostgroup.create({"name": "Frontend Hosts"})

druleIdFront = zapi.drule.get({"filter": { "name": "Frontend Discovery"}})
groupIdFront = zapi.hostgroup.get({"filter": {"name": "Frontend Hosts"}})

zapi.template.create({
    "host": "Template App Backend Service",
    "groups": {
        "groupid": groupIdFront[0].get("groupid")
    }
})
templateIdBackend = zapi.template.get({"output": "hostid","filter": {"name": "Template App Backend Service"}})
zapi.application.create({
    "name": "Backend Service",
    "hostid": templateIdBackend[0].get("templateid")
})
applicationIdBackend = zapi.application.get({"output": "hostids", "filter": {"name": "Backend Service"}})

zapi.item.create({
    "name": "Backend service is responding",
    "key_": "backend.is.running",
    "hostid": templateIdBackend[0].get("templateid"),
    "type": 0,
    "value_type": 3,
    "applications": [
        applicationIdBackend[0].get("applicationid")
    ],
    "delay": 5
})

zapi.trigger.create({
    "description": "Backend is down",
    "expression": "{Template App Backend Service:backend.is.running.last()}<>200",
    "priority" : 5
})

templateIdSoLinux=zapi.template.get({"output": "hostid","filter": {"name": "Template OS Linux"}})
templateIdHttp=zapi.template.get({"output": "hostid","filter": {"name": "Template App HTTP Service"}})

zapi.action.create({
    "name": "Frontend Action",
    "eventsource": "1",
    "status": "0",
    "esc_period": 0,
    "filter": {
        "evaltype": "0",
        "conditions": [{
            "operator": "0",
            "conditiontype": "18",
            "value": druleIdFront[0].get("druleid")
        }]
    },
    "operations": [
        {"operationtype": "2"},
        {
            "operationtype": "4",
            "opgroup": [{"groupid": groupIdFront[0].get("groupid")}]
        },{
            "operationtype": "6",
            "optemplate": [{"templateid": templateIdBackend[0].get("templateid")}],
        },{
            "operationtype": "6",
            "optemplate": [{"templateid": templateIdSoLinux[0].get("templateid")}],
        },{
            "operationtype": "6",
            "optemplate": [{"templateid": templateIdHttp[0].get("templateid")}],
        }],
})
druleIdBack = zapi.drule.get({"filter": { "name": "Backend Discovery"}})
groupIdBack = zapi.hostgroup.get({"filter": {"name": "Backend Hosts"}})

zapi.action.create({
    "name": "Backend Action",
    "eventsource": "1",
    "status": "0",
    "esc_period": 0,
    "filter": {
        "evaltype": "0",
        "conditions": [{
            "operator": "0",
            "conditiontype": "18",
            "value": druleIdBack[0].get("druleid")
        }]
    },
    "operations": [
        {"operationtype": "2"},
        {
            "operationtype": "4",
            "opgroup": [{"groupid": groupIdBack[0].get("groupid")}]
        },{
            "operationtype": "6",
            "optemplate": [{"templateid": templateIdSoLinux[0].get("templateid")}]
        }],
})







