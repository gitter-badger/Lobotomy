#!/usr/bin/env python
#
# Script.version    0.5
# Date:             03-07-2015
# Edited:           W Venhuizen
# Plugin:           autostart
#

import sys
import main
import time

Lobotomy = main.Lobotomy()


def autostart(database):
    case_settings = Lobotomy.get_settings(database)
    profile = case_settings["profile"]
    while profile is '0':
        print 'Waiting for imageinfo...'
        time.sleep(5)
        case_settings = Lobotomy.get_settings(database)
        profile = case_settings["profile"]
    """
    Add a line for every Lobotomy module you want to run when autostart is enabled
    You can use the following template:
        Lobotomy.add_to_queue('python modulename.py {}'.format(database))
    :param database: The database belonging to the memory dump
    :return:
    """

    autostart_db = Lobotomy.autostart_data('template')
    for row in autostart_db:
        if row[3] == 1:
            try:
                profile_db = row[5].split('|')
                for row_profile in profile_db:
                    if profile in row_profile:
                        command = row[2].replace('#', database)
                        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + command, row[6])
            except:
                pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: autostart.py <Database>"
    else:
        autostart(sys.argv[1])

