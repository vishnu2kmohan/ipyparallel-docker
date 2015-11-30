import os
import requests


MESOS_DNS_SRV_QUERY_TEMPLATE = \
   'http://master.mesos:8123/v1/services/_{0}._tcp.marathon.mesos'

if 'MARATHON_APP_ID' in os.environ:
    marathon_app_id = os.environ['MARATHON_APP_ID']
    app_srv_suffix = '-'.join(marathon_app_id.split('/')[:-1])
    # Assume 'controller' is embedded in app id - e.g., /<my-group>/controller
    app_srv = ''.join(['controller', app_srv_suffix])
    mesos_dns_srv_query_url = MESOS_DNS_SRV_QUERY_TEMPLATE.format(app_srv)
    r = requests.get(mesos_dns_srv_query_url)
    mesos_dns_srv_json = r.json()
    if 'engine' in marathon_app_id:
        # https://github.com/ipython/ipyparallel/blob/master/ipyparallel/factory.py
        # https://github.com/ipython/ipyparallel/blob/master/ipyparallel/controller/hub.py
        c.IPControllerApp.location = mesos_dns_srv_json[1]['host']
        c.RegistrationFactory.ip = '*'
        c.RegistrationFactory.regport = int(mesos_dns_srv_json[1]['port'])
