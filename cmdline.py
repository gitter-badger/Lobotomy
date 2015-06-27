__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "cmdline"

DEBUG = False


def main(database):
    Lobotomy.plugin_start('cmdline', database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + "-" + plugin + ".txt"
    
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

    p = 0
    cmd = 0
    with open(imagename + "-" + plugin + ".txt") as f:
        for line in f:
            if "pid:" in line:
                process = line.split(":")[0][:-4]
                pid = line.split(":")[1].strip(" ").strip("\n")
                p = 1
            if line.startswith("Command line :"):
                commandline = line.split(":",1)[1].strip("\n")
                commandline = commandline.replace('\\', '\\\\')

                cmd = 1
            if p != 0 and cmd != 0:
                SQL_cmd = "INSERT INTO cmdline VALUES (0, '{}', '{}', '{}')".format(process, pid, commandline)
                if DEBUG:
                    print SQL_cmd
                else:
                    Lobotomy.exec_sql_query(SQL_cmd, database)
                pid = 0
                cmd = 0

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
        Lobotomy.plugin_stop('cmdline', database)
        Lobotomy.plugin_pct(plugin, database, 100)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
