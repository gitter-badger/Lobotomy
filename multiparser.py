#!/usr/bin/env python

#
#   19-02 WV:   Aanpassen filenaam
#

#import re
import sys
import main
import os
from warnings import filterwarnings
filterwarnings('ignore')

DEBUG = False

Lobotomy = main.Lobotomy()


def multiparser(database, plugin):
    allowed_plugings = "atoms,atomscan,callbacks,clipboard,deskscan,driverscan,envars,filescan,gahti,gditimers,gdt,handles,hivelist,hivescan,idt,impscan,ldrmodules,memmap,messagehooks,modscan,modules,multiscan,objtypescan,prefetchparser,privs,pslist,psscan,pstree,psxview,shimcache,symlinkscan,thrdscan,timers,unloadedmodules,sockscan,netscan"
    allowed_plugings = allowed_plugings.split(",")
    if plugin in allowed_plugings:
        Lobotomy.plugin_start(plugin, database)
        Lobotomy.plugin_pct(plugin, database, 1)
        case_settings = Lobotomy.get_settings(database)
        imagename = case_settings["filepath"]
        imagetype = case_settings["profile"]
        casedir = case_settings["directory"]
        case = database    
        
        counter = 0
        
        command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + "-" + plugin + ".txt"
        
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        os.system(command)
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

        with open(imagename + "-" + plugin + ".txt") as f:
            result = []
            part = []
            linePointer = 0
            lastLinePointer = 0
            pointers = []

            for line in f:
                if counter == 1:
                    for x in line.split(' '):
                        pointers.append(len(x)+1)
                    pointers.pop(len(pointers)-1)
                    pointers.append(255)
                if counter > 1:
                    for x in range(len(pointers)): # Loop aantal kolommen
                        item = pointers[x]
                        lastLinePointer += item
                        part.append(line[linePointer:lastLinePointer].strip('\n').strip(' ')) # .strip("(v)").strip("(p)"
                        linePointer += item
                    linePointer = 0
                    lastLinePointer = 0
                    if DEBUG:
                        pass
                    result.append(part)
                counter += 1
                part = []

            Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start: running plugin: " + plugin)
            for listitem in result:
                if DEBUG:
                    print listitem
                else:
                    sql_line = "INSERT INTO " + plugin + " VALUES (0,"
                    for item in listitem:
                        item = item.replace('\\', '\\\\')
                        sql_line = sql_line + "'{}',".format(item)
                    sql_line = sql_line[:-1] + ")"
                    Lobotomy.exec_sql_query(sql_line, database)
            Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
            Lobotomy.plugin_stop(plugin, database)
            Lobotomy.plugin_pct(plugin, database, 100)
    else:
        print "plugin " + sys.argv[2] + " not supported"
        print "Usage: multiparser.py [Database] [plugin]"
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: multiparser.py [Database] [plugin]"
    else:
        multiparser(sys.argv[1], sys.argv[2])
