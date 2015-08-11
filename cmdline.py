__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.5
# 11 aug 2015:  WV
# Aanpasing van de huidige versie.
# Errormelding wordt gelogd in de case logfile
# Test met stuxnet en Windows 7 ging goed.

import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "cmdline"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)

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
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start:  running plugin: " + plugin)

    p = 0
    process = ''
    pid = ''
    commandline = ''
    with open(imagename + "-" + plugin + ".txt") as f:
        for line in f:
            if "pid:" in line:
                process = line.split(":")[0][:-4]
                pid = line.split(":")[1].strip(" ").strip("\n")
                p = 1
            if line.startswith("Command line :"):
                commandline = line.split(":", 1)[1].strip("\n")
                commandline = commandline.replace('\\', '\\\\')
            if p != 0 and line.startswith('*****'):
                SQL_cmd = "INSERT INTO cmdline VALUES (0, '{}', '{}', '{}')".format(process, pid, commandline)
                if DEBUG:
                    print SQL_cmd
                else:
                    try:
                        Lobotomy.exec_sql_query(SQL_cmd, database)
                    except:
                        print 'SQL Error in ', database, 'plugin: ', plugin
                        print 'SQL Error: ',  SQL_cmd
                        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Error:  running plugin: " + plugin)
                        Lobotomy.write_to_case_log(casedir, "Database: " + database + 'SQL line: ' + SQL_cmd)
                p = 0
                process = ''
                pid = ''
                commandline = ''

    # write last line to database
    SQL_cmd = "INSERT INTO cmdline VALUES (0, '{}', '{}', '{}')".format(process, pid, commandline)
    if DEBUG:
        print SQL_cmd
    else:
        try:
            Lobotomy.exec_sql_query(SQL_cmd, database)
        except:
            print 'SQL Error in ', database, 'plugin: ', plugin
            print 'SQL Error: ',  SQL_cmd
            Lobotomy.write_to_case_log(casedir, "Database: " + database + " Error:  running plugin: " + plugin)
            Lobotomy.write_to_case_log(casedir, "Database: " + database + 'SQL line: ' + SQL_cmd)
    p = 0
    process = ''
    pid = ''
    commandline = ''


    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
