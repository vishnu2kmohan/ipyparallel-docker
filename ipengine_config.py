import os
import requests

if 'MARATHON_APP_ID' in os.environ:
    marathon_app_id = os.environ['MARATHON_APP_ID']
    app_srv_prefix = '-'.join(marathon_app_id.split('/')[-1:])
    app_srv_suffix = '-'.join(marathon_app_id.split('/')[:-1])
    app_srv = ''.join(['controller', app_srv_suffix])
    mesos_dns_query_url = 'http://master.mesos:8123/v1/services/_{0}._tcp.marathon.mesos'.format(app_srv)
    r = requests.get(mesos_dns_query_url)
    if 'engine' in marathon_app_id:
        c.IPControllerApp.location = r.json()[1]['host']
        c.RegistrationFactory.ip = '*'
        c.RegistrationFactory.regport = int(r.json()[1]['port'])
