__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
###

import sys
import os
import main
Lobotomy = main.Lobotomy()

DEBUG = False


def main(database):
    plugin = "lobmftparser"
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + "-" + plugin + ".txt"
    
    Lobotomy.write_to_main_log(database, " Start: " + command)
    Lobotomy.write_to_case_log(casedir, " Start: " + command)
    if DEBUG:
        print command
#    else:
#        os.system(command)
    Lobotomy.write_to_main_log(database, " Stop : " + command)
    Lobotomy.write_to_case_log(casedir, " Stop : " + command)


    Lobotomy.write_to_case_log(casedir,"Database: " + database + " Start:  running plugin: " + plugin)
    with open(imagename + "-" + plugin + ".txt") as f:
    
        for line in f:
            if line.startswith("INSERT INTO mftparser VALUES (0,"):
                print line

#            SQL_cmd = "INSERT INTO getsids VALUES (0, '{}', '{}', '{}', '{}', '{}')".format(proc, pid, sid, user, comment)
#            if DEBUG:
#                print SQL_cmd
#            else:
#                Lobotomy.exec_sql_query(SQL_cmd, database)

    Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop:  running plugin: " + plugin)
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
