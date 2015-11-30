import os
import requests


MESOS_DNS_SRV_QUERY_TEMPLATE = 
   'http://master.mesos:8123/v1/services/_{0}._tcp.marathon.mesos'

if 'LIBPROCESS_IP' in os.environ:
    c.IPControllerApp.location = os.environ['LIBPROCESS_IP']

if 'MARATHON_APP_ID' in os.environ:
    marathon_app_id = os.environ['MARATHON_APP_ID']
    app_srv_prefix = '-'.join(marathon_app_id.split('/')[-1:])
    app_srv_suffix = '-'.join(marathon_app_id.split('/')[:-1])
    app_srv = ''.join([app_srv_prefix, app_srv_suffix])
    mesos_dns_srv_query_url = MESOS_DNS_SRV_QUERY_TEMPLATE.format(app_srv)
    r = requests.get(mesos_dns_srv_query_url)
    mesos_dns_srv_json = r.json()
    if 'controller' in marathon_app_id:
        # https://github.com/ipython/ipyparallel/blob/master/ipyparallel/factory.py
        # https://github.com/ipython/ipyparallel/blob/master/ipyparallel/controller/hub.py
        # IP on which to listen for client connections
        c.HubFactory.client_ip = '*'
        # IP on which to listen for engine connections
        c.HubFactory.engine_ip = '*'
        # IP on which to listen for monitor messages
        c.HubFactory.monitor_ip = '*'
        # The IP address for registration
        c.RegistrationFactory.ip = '*'
        # The port on which the Hub listens for registration
        c.RegistrationFactory.regport = int(mesos_dns_srv_json[1]['port'])
        # Client/Engine Port pair for Control Queue
        c.HubFactory.control = tuple([int(mesos_dns_srv_json[2]['port']), 
                                      int(mesos_dns_srv_json[3]['port'])])
        # PUB/ROUTER Port pair for Engine Heartbeats
        c.HubFactory.hb = tuple([int(mesos_dns_srv_json[4]['port']), 
                                 int(mesos_dns_srv_json[5]['port'])])
        # Client/Engine Port pair for IOPub relay (Tuple)
        c.HubFactory.iopub = tuple([int(mesos_dns_srv_json[6]['port']), 
                                    int(mesos_dns_srv_json[7]['port'])])
        # Monitor (SUB) port for queue traffic
        c.HubFactory.mon_port = int(mesos_dns_srv_json[8]['port'])
        # Client/Engine Port pair for MUX queue
        c.HubFactory.mux = tuple([int(mesos_dns_srv_json[9]['port']), 
                                  int(mesos_dns_srv_json[10]['port'])])
        # PUB port for sending engine status notifications
        c.HubFactory.notifier_port = int(mesos_dns_srv_json[11]['port'])
        # Client/Engine Port pair for Task queue
        c.HubFactory.task = tuple([int(mesos_dns_srv_json[12]['port']), 
                                   int(mesos_dns_srv_json[13]['port'])])
