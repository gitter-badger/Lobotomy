__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "ssdt"

DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + plugin + ".txt"
    
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
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  running plugin: " + plugin)

    ssdt = "tmp"
    mem1 = "123"
    entry = "123"
    mem2 = "123"
    systemcall = "tmp"
    owner = "tmp"

    try:
        with open(imagename + plugin + ".txt") as f:
            for line in f:
                #
                #[x86] Gathering all referenced SSDTs from KTHREADs...
                #Finding appropriate address space for tables...
                #SSDT[0] at 80501b8c with 284 entries
                #  Entry 0x0000: 0x80599948 (NtAcceptConnectPort) owned by ntoskrnl.exe
                #

                if ssdt != "tmp":
                    regel = line.strip("()").split(" ")
                    #print regel
                    try:
                        entry = regel[3]
                        mem2 = regel[4]
                        systemcall = regel[5].strip("()")
                        owner = regel[8].strip("\n")
                        SQL_cmd = "INSERT INTO ssdt VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(ssdt, mem1, entry, mem2, systemcall, owner)
    
                        if DEBUG:
                            print SQL_cmd
                        else:
                            Lobotomy.exec_sql_query(SQL_cmd, database)
                    except IndexError:
                        print "catch IndexError, continue"

                if line.startswith("SSDT"):
                    try:
                        ssdt, a, mem1, b, c, d = line.split(" ")
                    except ValueError:
                        if DEBUG:
                            print "ValueError on readline"
                        else:
                            Lobotomy.write_to_main_log(database, plugin + ": Error : ValueError on readline")

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
