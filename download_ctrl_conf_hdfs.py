#!/usr/bin/env python

import hdfs
import os


marathon_app_id = os.environ['MARATHON_APP_ID']
if 'engine' in marathon_app_id:
    app_path_prefix = '/'.join(marathon_app_id.split('/')[:-1])
    hdfs_ctrl_conf_path = ''.join(['/jupyter', 
                                   app_path_prefix, 
                                   '/ipcontroller-engine.json'])
    hdfs_client_conf_path = ''.join(['/jupyter', 
                                     app_path_prefix, 
                                     '/ipcontroller-client.json'])
    hdfs_url='http://namenode1.hdfs.mesos:50070/'
    hdfs_client = hdfs.InsecureClient(hdfs_url)
    hdfs_client.download(hdfs_ctrl_conf_path, 
                         '/home/conda/.ipython/profile_default/security/', 
                         overwrite=True)
    hdfs_client.download(hdfs_client_conf_path, 
                         '/home/conda/.ipython/profile_default/security/', 
                         overwrite=True)
