__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
import MySQLdb
import time
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "hivedump"

DEBUG = False

def main(database, offset):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " -o " + offset + " > " + imagename +  "-" + plugin + "-" + offset + ".txt"
    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        os.system(command)
        pass
        
    if DEBUG:
        print "Write log: " + database + " ,Stop: " + command
        print "Write log: " + casedir + " ,Stop: " + command
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,"Database: " + database + " Start:  running plugin: " + plugin)

    #with open(imagename + plugin + ".txt") as f:
    #    for hiveitem in f:
    #    
    #        # Hivelist om de offsets te verkrijgen
    #        # Hivedump om de hivelistings te verkrijgen
    #        # printkeys om door de hives te itereren.
    #
    #        # hivelist > memfor3nov.vmemhivelist.txt
    #        #Virtual    Physical   Name
    #        #---------- ---------- ----
    #        #0xe2273008 0x1684c008 \Device\HarddiskVolume1\Documents and Settings\Chris Balt\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat
    #        #0xe229f008 0x1687e008 \Device\HarddiskVolume1\Documents and Settings\Chris Balt\NTUSER.DAT
    #
    #        
    #        SQL_cmd = 0
    #        if hiveitem.startswith("0x"):
    #            virtual, physical, hivefilepath = hiveitem.split(" ", 2)
    #            virtual = MySQLdb.escape_string(virtual)
    #            physical = MySQLdb.escape_string(physical)
    #            #hivefilepath = hivefilepath.replace('\\', '\\\\').strip("\n")
    #            hivefilepath = hivefilepath.strip("\n")
    #            hivefilepath = MySQLdb.escape_string(hivefilepath)
    #            SQL_cmd = "INSERT INTO hivelist VALUES (0, '{}', '{}', '{}')".format(virtual, physical, hivefilepath)
    #            if DEBUG:
    #                print SQL_cmd
    #            else:
    #                Lobotomy.exec_sql_query(SQL_cmd, database)
    #                pass
    #            command = "vol.py -f " + imagename + " --profile=" + imagetype + "  hivedump -o " + virtual + " >> " + imagename + "hivedump.txt"
    #            os.system(command)
    #            
    #
    #try:
    with open(imagename +  "-" + plugin + "-" + offset + ".txt") as f:
        for hiveitemkey in f:
            SQL_cmd = 0
            if not hiveitemkey.startswith("Last Written"):
                lastwritten = hiveitemkey[0:28]
                lastwritten = parse(lastwritten).strftime("%Y-%m-%d %H:%M:%S")
                key = hiveitemkey[29:]
                key = key.strip("\n")
                key = MySQLdb.escape_string(key)
                strippedkey = 0
                if key.startswith("\\\\$$$") or key.startswith("\\\\S-1-5") or key.startswith("\\\\SAM") \
                        or key.startswith("\\\\CMI"):
                    try:
                        key = key.split("\\", 3)[3][1:]
                    except:
                        key = key.split("\\", 3)[2][1:]
                    strippedkey = 1
                SQL_cmd = "INSERT INTO hivedump VALUES (0, '{}', '{}')".format(lastwritten, key)
                if DEBUG:
                    print SQL_cmd
                else:
                    Lobotomy.exec_sql_query(SQL_cmd, database)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop:  running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename> <offset>"
    else:
        main(sys.argv[1], sys.argv[2])
