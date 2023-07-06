#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WeWorkflow, an Alfred workflow to access workflow info, folders etc. 
# rewritten from "Manage Alfred Extension" by Jaemok Jeong, 2013/3/25 http://jmjeong.com
# Partly cloudy ⛅️  🌡️+54°F (feels +53°F, 40%) 🌬️↓2mph 🌕 Fri Apr 15 06:50:32 2022


import os
import sys
import json
import sqlite3
from WeWorkflow_functions import *
from config import INDEX_DB, CACHE_FOLDER, DIRNAME, DATA_FOLDER
import time


startTimeJ = time.time()

# checking timestamps to determine if the database needs to be rebuilt
# this function will also fetch plists, rebuild database and update timestamp
checkingTime(DIRNAME)



query = sys.argv[1]




# Search!
db = sqlite3.connect(INDEX_DB)
cursor = db.cursor()


resultJ = {"items": []}



cursor.execute("""SELECT description,name,disabled, createdby, version, keywords, hotkeys, path, timestamp, hot_duplicated, bundleid, author FROM
                    (SELECT workflows
                        AS  r, description, name,disabled, createdby, version, keywords, hotkeys, path, timestamp, hot_duplicated, bundleid, author
                        FROM workflows) ORDER BY name COLLATE NOCASE""")
if query:
    cursor.execute("""SELECT description,name,disabled, createdby, version, keywords, hotkeys, path, timestamp, hot_duplicated, bundleid, author FROM
                        (SELECT workflows
                            AS  r, description, name,disabled, createdby, version, keywords, hotkeys, path, timestamp, hot_duplicated, bundleid, author
                            FROM workflows WHERE workflows MATCH ?) ORDER BY name COLLATE NOCASE""", (query + '*',))
    
resultsQ = cursor.fetchall()

# Output results to Alfred
if (resultsQ):
    
    myResLen = str(len (resultsQ))
    countR=1
    #log (countR)
    
    for (description, name,disabled, createdby, version, keywords,hotkeys, path, timestamp, hot_duplicated, bundleid,author) in resultsQ:
        # resetting all the string blocks
        disabledString=''
        keywordsString = ''
        hotkeyString = ''

    
        if disabled == "True":
            disabledString = " (disabled)"
        if keywords:
            keywordsString = " 🔑"+keywords
        
        if hotkeys:
            hotkeyString = " 🔥"+hotkeys
        

        lastModified = time.strftime('%Y-%m-%d, %H:%M', time.localtime(int(timestamp)))
        if hot_duplicated != '':
            conflictString = "conflicts: " + hot_duplicated
        else:
            conflictString = ''
        
        mySummary = \
        name + " " +  version + "\n"+\
        "by: " + createdby+ "\n"+\
            description + "\n"+\
            "last modified: " +lastModified+     "\n"+\
            keywordsString+ "\n"+\
            hotkeyString + "\n\n"+ \
            conflictString 

        
            #add: 1) last modified

        myCachePath=CACHE_FOLDER+bundleid
        if not os.path.exists(myCachePath):
            cacheString = "no cache folder to open "
        else:
            cacheString = "Open cache folder "

        myDataPath=DATA_FOLDER+bundleid
        if not os.path.exists(myDataPath):
            dataString = "no data folder to open "
        else:
            dataString = "Open data folder "

        resultJ["items"].append({
            "title": name+disabledString,
            "subtitle": str(countR)+"/"+myResLen + " "+description + "-"+createdby+keywordsString+hotkeyString,
             "variables": {
                 "mySummary": mySummary,
                 "myPath": path,
                 "myFirstKey": keywords.split(",")[0],
                 "myBundleID": bundleid,
                 "myWorkflow": name,
                 "myCachePath": myCachePath,
                 "myDataPath": myDataPath
             },
            "valid": True,
            "arg": path,
            "mods": {
    
    
            "option": {
                "valid": 'true',
                "subtitle": cacheString+"in Finder"
            },
            "option+shift": {
                "valid": 'true',
                "subtitle": cacheString+"in Terminal"
            },
            "option+ctrl+shift": {
                "valid": 'true',
                "subtitle": dataString+"in Finder"
            }
            },
            "icon": {
                "path": path+"/icon.png"
                }
            })
        countR += 1  
        

    executionTime = (time.time() - startTimeJ)
    log ("time to query: "+ str(executionTime))
    

    print (json.dumps(resultJ))
    

if (query and not resultsQ):
    result= {"items": [{
    "title": "No matches",
    "subtitle": "Try a different query",
    
    "arg": "",
    "icon": {

            "path": "icons/Warning.png"
        }
    }]}
    
    print (json.dumps(result))
    
