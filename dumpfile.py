__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "Bulk_Extractor"

DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/dump_bulk"
    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass
    command = "bulk_extractor -o " + dumpdir + " -e all " + imagename
    #command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " --dump-dir=" + dumpdir
    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        log = ""
        status, log = commands.getstatusoutput(command)
        
    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  Running Bulk_Extractor: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  Running Bulk_Extractor: " + plugin)
        
#    counter = 0
#    result = []
#    part = []
#    linePointer = 0
#    lastLinePointer = 0
#    pointers = []
#
#    #if DEBUG:
#    #    print vollog
#    #else:
#    #    vollog = vollog.split("\n")
#    vollog = vollog.split("\n")
#    for line in vollog:
#        if counter == 2:
#            for x in line.split(' '):
#                pointers.append(len(x)+1)
#            pointers.pop(len(pointers)-1)
#            pointers.append(255)
#        if counter > 2:
#            for x in range(len(pointers)): # Loop aantal kolommen
#                item = pointers[x] 
#                lastLinePointer += item
#                part.append(line[linePointer:lastLinePointer].strip('\n').strip(' '))
#                linePointer += item
#            linePointer = 0
#            lastLinePointer = 0
#            if DEBUG:
#                pass
#            result.append(part)
#        counter += 1
#        part = []
#
#    for listitem in result:
#        if DEBUG:
#           print listitem
#        else:
#            sql_line = "INSERT INTO " + plugin + " VALUES ("
#            for item in listitem:
#                item = item.replace('\\', '\\\\')
#                sql_line = sql_line + "'{}',".format(item)
#                if item == listitem[3] and item.startswith("OK:"):
#                    md5 = Lobotomy.md5Checksum(dumpdir + "/" + listitem[3].strip("OK: "))
#                else:
#                    md5 = "0"
#                #sql_line = sql_line 
#            sql_line = sql_line + "'" + md5 + "'" +")"
#            #sql_line = sql_line[:-1] + ")"
#            Lobotomy.exec_sql_query(sql_line, database)
    
    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin + ")"
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin)

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
