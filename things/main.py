#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py, v1.0
#
# Jaemok Jeong, 2016/11/15


import re
import sys
import unicodedata
import json
from datetime import date, timedelta

import util

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    try: q = unicodedata.normalize('NFC',  unicode(sys.argv[1].strip()))
    except: q = ""

    (title, tag, day, note) = util.parse(q)

    if day:
        title = title + '> ' + day.strftime('%m/%d %a')
    else:
        title = title

    subtitle = "title #tag1 #tag2 ::note >duedate (ex. fri, 3d, 2w, 12/31)"
    help = {"valid": False, "subtitle": subtitle}
    
    output = []
    output.append({"title": title, "subtitle": subtitle, "arg":q, "valid": True,
                  "mods": { "alt": help, "ctrl":help, "cmd":help, "shift":help}})
    print json.dumps({"items": output})


if __name__ == '__main__':
    main()
