#!/usr/bin/env python

import sys
import main

Lobotomy = main.Lobotomy()


def autostart(database):
    case_settings = Lobotomy.get_settings(database)
    profile = case_settings["profile"]
    """
    Add a line for every Lobotomy module you want to run when autostart is enabled
    You can use the following template:
        Lobotomy.add_to_queue('python modulename.py {}'.format(database))
    :param database: The database belonging to the memory dump
    :return:
    """
    if profile.startswith('Win'):
        Lobotomy.write_to_main_log(database, "Executing autostart.py for {}".format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'memtimeliner.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} pslist'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} psscan'.format(database))
        #Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} pstree'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} psxview'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} atoms'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dlllist.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'cmdscan.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'cmdline.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'ssdt.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'getsids.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} driverscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} envars'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} filescan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} handles'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} callbacks'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} clipboard'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} thrdscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'multiparser.py {} atomscan'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpproc.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpdll.py {}'.format(database))
        Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'dumpfile.py {}'.format(database))
    if profile == "WinXPx86" or profile == "WinXPSP2x86" or profile == "WinXPSP3x86":
        pass # Sockscan, connections, connscan, sockets, sockscan
    if profile == "WinVistaX86" or profile == "Win7SP1x86" or profile == "Elke andere windows vista+ machine":
        pass # netscan

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: autostart.py <Database>"
    else:
        autostart(sys.argv[1])
