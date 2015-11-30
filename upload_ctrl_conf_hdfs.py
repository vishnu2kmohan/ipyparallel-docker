#!/usr/bin/env python

import os
import hdfs


marathon_app_id = os.environ['MARATHON_APP_ID']
if 'controller' in marathon_app_id:
    app_path_prefix = '/'.join(marathon_app_id.split('/')[:-1])
    hdfs_path_prefix = ''.join(['/jupyter', app_path_prefix])
    hdfs_url='http://namenode1.hdfs.mesos:50070/'
    hdfs_client = hdfs.InsecureClient(hdfs_url)
    hdfs_client.makedirs(hdfs_path_prefix)
    hdfs_client.upload(hdfs_path_prefix, 
        '/home/conda/.ipython/profile_default/security/ipcontroller-engine.json', 
        overwrite=True)
    hdfs_client.upload(hdfs_path_prefix, 
        '/home/conda/.ipython/profile_default/security/ipcontroller-client.json', 
        overwrite=True)
