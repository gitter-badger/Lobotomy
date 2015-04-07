__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
#   19-02   WV: Opschonen code, aanpassen bestandnaam
#

import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "none"

DEBUG = False


def main(database):
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

    try:
        with open(imagename + "-" + plugin + ".txt") as f:
            for line in f:

                if line.startswith("**********************"):
                    linenr = 0
                    dll = 0
                else:
                    linenr += 1
                    if linenr == 1:
                        a, b = line.split(":")
                        proc = a.split(" ")[0]
                        pid = b.strip(" ").strip("\n")
                    if linenr == 2:
                        if line.startswith("Command"):
                            cmd = line.split(": ")[1].strip("\n")
                        else:
                            cmd = line.strip("\n")
                    if linenr == 3:
                        if line.startswith("Service"):
                            sp = line
                        else:
                            sp = ""
                    if dll == 1:
                        base = line[0:10].strip(" ")
                        size = line[11:22].strip(" ")
                        loadcount = line[23:33].strip(" ")
                        path = line[33:]
                        path = path.replace('\\', '\\\\')
                    if line.startswith("----------"):
                        dll = 1
                    if proc != "" and dll == 1:
                        SQL_cmd = "INSERT INTO dlllist VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(proc, pid, cmd, sp, base, size, loadcount, path)
                        if DEBUG:
                            print SQL_cmd
                        else:
                            Lobotomy.exec_sql_query(SQL_cmd, database)
    except IOError:
        print "IOError, file not found."
        if DEBUG:
            print "Debug mode is on: try creating a sample file."

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
