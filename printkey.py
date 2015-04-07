__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
import MySQLdb
import time
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "printkey"

DEBUG = False

def main(database, regkey):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " -K '" + regkey + "' > " + imagename + "-" + plugin + ".txt"
    
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


    
    newkey = 0
    value = 0
    with open(imagename + "-" + plugin + ".txt") as f:
        for line in f:
            change = 0
            if line.startswith("-----"):
                newkey = 1
                value = 0
                newkey = 0
                register = 0
                keyname = 0
                keylegend = 0
                lastupdated = 0
                subkeys = 0
                type = 0
                values = 0
                legend = 0
                threadingmodel = 0
            if line.startswith("Registry"):
                register = line.split(" ", 1)[1]
                #register = register.replace('\\', '\\\\').strip("\n")
                register = register.strip("\n")
                register = MySQLdb.escape_string(register)
            if line.startswith("Key name"):
                keyname = line.split(":", 1)[1][1:].split(" ")[0]
                keylegend = line.split(":")[1].split("(")[1][0]
                keyname = MySQLdb.escape_string(keyname)
            if line.startswith("Last updated"):
                lastupdated = line.split(" ", 2)[2]
                lastupdated = parse(lastupdated).strftime("%Y-%m-%d %H:%M:%S")
            if line.startswith("  (S)"):
                change = 1
                subkeys = line.split(")", 1)[1][1:]
                subkeys = subkeys.replace('\\', '\\\\').strip("\n")
                subkeys = MySQLdb.escape_string(subkeys)
            if value == 1 and not line.startswith("Legend"):
                change = 1
                try:
                    type = line.split(" ",1)[0]
                    model = line[14:]
                    model = model.strip(" ").split(":")[0]
                    legend = line.split(":",1)[1][2]
                    values = line.split(":",1)[1][5:]
                    values = values.replace('\\', '\\\\').strip("\n")
                    values = MySQLdb.escape_string(values)
                except:
                    pass
                if change == 1:
                    SQL_cmd = "INSERT INTO printkey VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(register, keyname, keylegend, lastupdated, subkeys, type, values, legend, model)
                    if DEBUG:
                        print SQL_cmd
                        newkey = 0
                    else:
                        try:
                            Lobotomy.exec_sql_query(SQL_cmd, database)
                        except:
                            print "Error: SQL statement error. Error op binaire data. " , SQL_cmd
                        newkey = 0
            if line.startswith("Values:"):
                value = 1
                
                        #----------------------------
                        #Registry: \Device\HarddiskVolume1\Documents and Settings\Chris Balt\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat
                        #Key name: {CAFEEFAC-0014-0002-0015-ABCDEFFEDCBB} (S)
                        #Last updated: 2013-03-14 14:19:33 UTC+0000
                        #
                        #Subkeys:
                        #  (S) InprocServer32
                        #
                        #Values:
                        #REG_SZ                        : (S) Java Plug-in 1.4.2_15 
                        #REG_SZ        ThreadingModel  : (S) Apartment 
                        
    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename> <key>"
    else:
        main(sys.argv[1], sys.argv[2])
