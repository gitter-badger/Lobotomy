#!/usr/bin/env python
#
# Script.version    0.2
# Date:             14-05-2015
# Edited:           W Venhuizen
# Plugin:           autostart
#
# PR_dump.py toegevoegd aan de queue
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
        time.sleep(1)
        case_settings = Lobotomy.get_settings(database)
        profile = case_settings["profile"]
    """
    Add a line for every Lobotomy module you want to run when autostart is enabled
    You can use the following template:
        Lobotomy.add_to_queue('python modulename.py {}'.format(database))
    :param database: The database belonging to the memory dump
    :return:
    """
    if profile.startswith("Win"):
        Lobotomy.write_to_main_log(database, "Executing autostart.py for {}".format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'memtimeliner.py {}'.format(database), 4)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} pslist'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'pstree.py {}'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'consoles.py {}'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'cmdline.py {}'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'hivelist.py {}'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} handles'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} clipboard'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} ldrmodules'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} psscan'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'prefetchparser.py {}'.format(database), 3)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} psxview'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} atoms'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dlllist.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'cmdscan.py {}'.format(database), 4)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'ssdt.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'getsids.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} driverscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} envars'.format(database), 2)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} filescan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} callbacks'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} thrdscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} atomscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpproc.py {}'.format(database), 4)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpdll.py {}'.format(database), 4)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpfile.py {}'.format(database), 6)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'PR_dump.py {}'.format(database), 5)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} clipboard'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} gahti'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} gditimers'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} gdt'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} getservicesids'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} idt'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} joblinks'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} memmap'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} modscan'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} modules'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} mutantscan'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} objtypescan'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} privs'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} shimcache'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} symlinkscan'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} timers'.format(database), 10)
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} unloadedmodules'.format(database), 10)

        #Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} userhandles'.format(database), 10)
        #Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} vadwalk'.format(database), 10)

    #if 'XP' in profile:
    if profile.startswith("WinXP"):
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'sockets.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'sockscan.py {}'.format(database))
        pass # connections, connscan,  sockscan
#    if profile == "WinVistax86" or profile == "Win7SP1x86" or profile == "Win7SP1x64" or profile == "Elke andere windows vista+ machine":
#        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'netscan.py {}'.format(database))
    if 'Win7' in profile or 'Vista' in profile:
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'netscan.py {}'.format(database))

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: autostart.py <Database>"
    else:
        autostart(sys.argv[1])

