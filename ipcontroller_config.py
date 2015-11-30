import os
import requests
from traitlets import Tuple

if 'LIBPROCESS_IP' in os.environ:
    c.IPControllerApp.location = os.environ['LIBPROCESS_IP']

if 'MARATHON_APP_ID' in os.environ:
    marathon_app_id = os.environ['MARATHON_APP_ID']
    app_srv_prefix = '-'.join(marathon_app_id.split('/')[-1:])
    app_srv_suffix = '-'.join(marathon_app_id.split('/')[:-1])
    app_srv = ''.join([app_srv_prefix, app_srv_suffix])
    mesos_dns_query_url = 'http://master.mesos:8123/v1/services/_{0}._tcp.marathon.mesos'.format(app_srv)
    r = requests.get(mesos_dns_query_url)
    if 'controller' in marathon_app_id:
        # IP on which to listen for client connections
        c.HubFactory.client_ip = '*'
        # IP on which to listen for engine connections
        c.HubFactory.engine_ip = '*'
        # IP on which to listen for monitor messages
        c.HubFactory.monitor_ip = '*'
        c.RegistrationFactory.ip = '*'
        c.RegistrationFactory.regport = int(r.json()[1]['port'])
        # Client/Engine Port pair for Control Queue
        c.HubFactory.control = tuple([int(r.json()[2]['port']), 
                                      int(r.json()[3]['port'])])
        # PUB/ROUTER Port pair for Engine Heartbeats
        c.HubFactory.hb = tuple([int(r.json()[4]['port']), 
                                 int(r.json()[5]['port'])])
        # Client/Engine Port pair for IOPub relay (Tuple)
        c.HubFactory.iopub = tuple([int(r.json()[6]['port']), 
                                    int(r.json()[7]['port'])])
        # Monitor (SUB) port for queue traffic
        c.HubFactory.mon_port = int(r.json()[8]['port'])
        # Client/Engine Port pair for MUX queue
        c.HubFactory.mux = tuple([int(r.json()[9]['port']), 
                                  int(r.json()[10]['port'])])
        # PUB port for sending engine status notifications
        c.HubFactory.notifier_port = int(r.json()[11]['port'])
        # Client/Engine Port pair for Task queue
        c.HubFactory.task = tuple([int(r.json()[12]['port']), 
                                   int(r.json()[13]['port'])])
