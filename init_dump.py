#!/usr/bin/python

import os
import sys
import string
import random
import time


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

collect_dir = '/dumps/'
store_dir = '/cases/'
dumpname = sys.argv[1]


def parse_cfg():
    configfile = collect_dir + dumpname.split('.', 1)[0] + '.ini'
    from configobj import ConfigObj
    config = ConfigObj(configfile)
    try:
        profile = config['profile']
    except KeyError:
        profile = 'None'
    try:
        comments = config['comments']
    except KeyError:
        comments = 'None'
    try:
        autostart = config['autostart']
    except KeyError:
        autostart = 'No'
    return [profile, comments, case_id, autostart]

if os.path.isfile(collect_dir + dumpname):
    profile = comments = case_id = autostart = 'None'
    if os.path.isfile(collect_dir + dumpname.split('.', 1)[0] + '.ini'):
        profile, comments, case_id, autostart = parse_cfg()
    prefix = str(time.strftime("%y%m%d%H%M")) + '_'
    print prefix + dumpname
    print "Profile:    ", profile
    print "Case ID:    ", case_id
    print "Comments:   ", comments
    print "Auto-start: ", autostart