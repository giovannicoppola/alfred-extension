#!/usr/bin/env python3

import os


WF_BUNDLE = os.getenv('alfred_workflow_bundleid')
WF_FOLDER = os.path.expanduser('~')+"/Library/Caches/com.runningwithcrayons.Alfred/Workflow Data/"+WF_BUNDLE+"/"
CACHE_FOLDER = os.path.expanduser('~')+"/Library/Caches/com.runningwithcrayons.Alfred/Workflow Data/"
DATA_FOLDER = os.path.expanduser('~')+"/Library/Application Support/Alfred/Workflow Data/"


INDEX_DB = WF_FOLDER+"index.db"
TIMESTAMP = WF_FOLDER+'timestamp.txt'

DIRNAME = os.path.dirname(os.path.abspath('.'))

if not os.path.exists(WF_FOLDER):
    os.makedirs(WF_FOLDER)

if not os.path.exists(TIMESTAMP):
    with open(TIMESTAMP, "w") as f:
        f.write('1604584800') # put a random date in 2020 as starting date 
        f.close
    
    