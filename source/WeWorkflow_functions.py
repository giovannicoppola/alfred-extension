#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Functions for WeWorkflow: 
# log (for logging and debugging)
# checkingTime (to checktimestamps)
# JSONtoDB (to rebuild the database)


import sys
import os
import sqlite3
import time
import plistlib
import unicodedata

startTime = time.time()

from config import TIMESTAMP, INDEX_DB

## checking the timestamp
with open(TIMESTAMP) as f:
    old_time = int(f.readline()) #getting the old UNIX timestamp
    f.close


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def checkingTime (dirname):
## Checking if the index needs to be rebuilt
# one other option was to add everything to a list then choose the max. 
# advantage: I already have the max to add it to the timestamp
# disadvage: needs to go through all dirs, while with the other method you can break as soon one is more recent than the timestamp

    dirs = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
    

    for (idx,d) in enumerate(dirs): # goes through each directory looking for a plist file. idx is a counter from enumerate, d is the directory (and plist file) name
        try:
            myPlist = (os.path.join(dirname, d, 'info.plist'))
            myTime= (int(os.path.getmtime(myPlist)))
            #log (idx)
            # this should be faster because it breaks when it finds one
            if myTime >= old_time:
                log ("found an updated plist file, rebuilding the database")
                #fetching all the plists and rebuilding the database
                fetchPlists (dirname)
                return "toBeUpdated"
        except:
            continue
    executionTime = (time.time() - startTime)
    log ("time to check timestamps: "+ str(executionTime))
    log ("database uptodate")


def fetchPlists(dirname):

    # this information is borrowed from (com.help.shawn.rice) by Shawn Rice
    hotmod = {
                    131072 : "sht",
                    262144 : "ctl",
                    262401 : "ctl", # https://github.com/shawnrice/alfred2-workflow-help/pull/2/files
                    393216 : "sht-ctl",
                    524288 : "opt",
                    655360 : "sht-opt",
                    786432 : "ctl-opt",
                    917504 : "sht-ctl-opt",
                    1048576 : "cmd",
                    1179648 : "sht-cmd",
                    1310720 : "ctl-cmd",
                    1310985 : "ctl-cmd", 
                    1441792 : "sht-ctl-cmd",
                    1572864 : "opt-cmd",
                    1703936 : "sht-opt-cmd",
                    1835008 : "ctl-opt-cmd",
                    1966080 : "sht-ctl-opt-cmd"
    }

    
    dirs = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
    allPlists = []


    for (idx,d) in enumerate(dirs): # goes through each directory looking for a plist file. idx is a counter from enumerate, d is the directory (and plist file) name
        try:
            myPlistPath = (os.path.join(dirname, d, 'info.plist'))
            myPath = (os.path.join(dirname, d))
            myTimeStamp = (int(os.path.getmtime(myPlistPath)))
            with open(myPlistPath, 'rb') as fp:
                myPlist = plistlib.load(fp)
                myPlist ['path'] = myPath
                myPlist ['timestamp'] = myTimeStamp
                myPlist ['author'] = remove_accents(myPlist['createdby'])
                myPlist['hot_duplicated'] = ''
        except:
            continue
        
        try:
            #keywords in each workflow, comma delimited
            
            # this command below did not work for all workflows, because some script filters don't have a keyword set. 
            #myKeywords = ",".join([o['config']['keyword'].strip() for o in myPlist['objects'] if 'alfred.workflow.input' in o['type']]) 
            
            # replaced with a less elegant, but working loop:
            myKeys=[]
            myObjects = myPlist['objects']
            for o in myObjects:
                if ('alfred.workflow.input' in o['type']) and ('keyword' in o['config']):
                    myKeys.append (o['config']['keyword'])
                
            myKeywords = ",".join(x.strip() for x in myKeys)
            
        except KeyError:
            myKeywords = ""
                
        myPlist['Keywords'] = myKeywords  # adding keywords to the dict with all the plist
        
        
        try:
            # finding all the hotkeys in each workflow (comma separated), use hotmod to convert the ID to a string
            myHotkeys = ",".join([hotmod[o['config']['hotmod']]+"-"+o['config']['hotstring'].lower()
                                for o in myPlist['objects']
                                if 'alfred.workflow.trigger.hotkey' in o['type']
                                and o['config']['hotmod'] != 0 and o['config']['hotkey'] != 0])
        except KeyError:
                myHotkeys = ""
                
        
        myPlist['Hotkeys'] = myHotkeys  # adding hotkeys to the dict with all the plist
            
        allPlists.append(myPlist) # adding the plist with new fields to the master list used to create the db

    ## creating a list of all hotkeys, another unique
    hotkey_list = []
    hotkey_duplicated = []

    for myRecords in allPlists:
        if myRecords['Hotkeys']: 
            myKeys = myRecords['Hotkeys'].split(',')
            for myKey in myKeys:
                hotkey_list.append(myKey)

    #check which keys are duplicated     
    for myKey in hotkey_list:
        if hotkey_list.count(myKey) >1:
            if myKey not in hotkey_duplicated:
                hotkey_duplicated.append(myKey)

    #log (hotkey_duplicated)
    firstTag_flag = 0        
    for myDupKey in hotkey_duplicated:
        first_flag = 0
        enable_count = 0
        disable_count = 0
        for myRecord in allPlists:
            if myDupKey in myRecord['Hotkeys']:
                if first_flag == 0 and firstTag_flag == 0:
                    myDupString = "["+myDupKey+"]: "+myRecord['name']
                    first_flag = 1
                    firstTag_flag = 1
                elif first_flag == 0 and firstTag_flag != 0:
                    myDupString = myDupString + " - "+ "["+ myDupKey+"]: "+myRecord['name']
                    first_flag = 1
                else:
                    myDupString = myDupString + ", "+myRecord['name']
                if myRecord['disabled'] == True:
                    disable_count += 1 
                    myDupString = myDupString + " (disabled)"
                else:
                    enable_count += 1 
                    
     
        for myRecord in allPlists: #goes again through the records to update them with the complete string and appropriate symbol
            
            if myDupKey in myRecord['Hotkeys']:
                #log (myDupKey+ "-"+ myRecord['name'] + "-"+ str(enable_count)+ "-"+ str(disable_count))    
                myRecord['hot_duplicated'] = myDupString
                if ((enable_count == 1) and (disable_count >= 1)): # if only one enabled and one or more disabled share the hotkey, use a different symbol
                    myRecord['Hotkeys'] = myRecord['Hotkeys'].replace (myDupKey,myDupKey+"🟠")
                    #log ("making the 🟠 replacement")
                else:
                    #log ("making the 🔴 replacement in " +myRecord['name'])
                    myRecord['Hotkeys'] = myRecord['Hotkeys'].replace (myDupKey,myDupKey+"🔴")
    
    # recreating the database
    JSONtoDB (allPlists,'workflows',INDEX_DB)
    
    with open(TIMESTAMP, "w") as f:
        f.write(str(round (startTime))) # update the timestamp
    f.close
                    
                    
     
                
        
     
    


def JSONtoDB (myJSON,myTable, mydatabase):
    column_list = []
    column = []
    for data in myJSON:
        
        column = list(data.keys())
        for col in column:
            if col not in column_list:
                column_list.append(col)

    value = []
    values = [] 
    for data in myJSON:
        for i in column_list:
            value.append(str(dict(data).get(i)))   
        values.append(list(value)) 
        value.clear()
        
    
    
    create_statement = "create VIRTUAL table " + myTable + " USING FTS3 ({0})".format(" text,".join(column_list))
      
    insert_statement = "insert into " + myTable + " ({0}) values (?{1})".format(",".join(column_list), ",?" * (len(column_list)-1))    
    drop_statement = "DROP TABLE IF EXISTS "+ myTable  

    # execution	
    db=sqlite3.connect(mydatabase)
    c = db.cursor()   
    c.execute(drop_statement)
    c.execute(create_statement)
    c.executemany(insert_statement , values)
    values.clear()
    db.commit()






