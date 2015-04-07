__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
### 18-02: WV - Kleine aanpassing en opschonen script.
###

import sys
import os
import main
import MySQLdb
Lobotomy = main.Lobotomy()
plugin = "strings"

DEBUG = False

def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "strings -tx " + imagename + " > " + imagename + "-" + plugin + ".txt"
    
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

    with open(imagename + "-" + plugin + ".txt") as f:
        SQL_cmd = ""
        for line in f:
            x, y = line.strip("  ").split(" ", 1)
            y = y.strip("\n")
            if y == "":
                y = 0
            y = MySQLdb.escape_string(y)
            SQL_cmd = "INSERT INTO strings VALUES (id, '{}', '{}')".format(x, y)
            if DEBUG:
                print SQL_cmd
            else:
                Lobotomy.exec_sql_query(SQL_cmd, database)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop:  running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
