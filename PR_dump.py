__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.2
# Date:             05-05-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Edited:           W Venhuizen
# Parsing photorec logfile en bereken md5 over files.
# kleine aanpassing in console output. geen info is net te weinig als het lang duurt, voor screen maakt output niet uit.

import sys
import os
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "PhotoRec"


DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/pr_dump"
    pct = 0

    Lobotomy.plugin_pct(plugin, database, 0)
    print "pct done: " + str(pct)

    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass

    command = "photorec /debug /log /logname " + casedir + "/photorec.log /d " + dumpdir + " /cmd " + imagename + " fileopt,everything,enable,search"

    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start:  Running PhotoRec: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  Running PhotoRec: " + plugin)

    if DEBUG:
        print command
    else:
        print "Running Photorec. Please wait."
        log = ""
        status, log = commands.getstatusoutput(command)

    Lobotomy.plugin_pct(plugin, database, 25)
    print "pct done: " + str(25)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running PhotoRec: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Stop:  Running PhotoRec: " + plugin)

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)
    
    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin + ")"
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin)

    # parse reports.xml
    # parse photorec.log
    # casedir + "/photorec.log
    counter = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
            if line.startswith(casedir):
                filenaam = line.split("\t")[0]
                if not filenaam.endswith("mft"):
                    counter += 1
    Lobotomy.plugin_pct(plugin, database, 30)
    print "pct done: " + str(30)
    print "Parsing Photorec logfile"

    #
    # percentage done = 25%
    # bereken percentage van md5 sum e.d. tot 50%, dus 25 procent.
    # counter is aantal te berekenen files. dus counter is 100% van de files.
    # pct = 25 / counter * count
    count = 0
    pcttmp = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
            if line.startswith(casedir):
                filenaam = line.split("\t")[0]
                if not filenaam.endswith("mft"):
                    count += 1
                    try:
                        filemd5 = Lobotomy.md5Checksum(filenaam)
                    except:
                        pass
                    pct = str(float(1.0 * count / counter) * 25).split(".")[0]
                    filename = filenaam.split("/")[-1]
                    SQL_cmd = "INSERT INTO PR_files VALUES (0, '{}', '{}', '{}')".format(filenaam, filename, filemd5)
                    if DEBUG:
                        print SQL_cmd
                    else:
                        Lobotomy.exec_sql_query(SQL_cmd, database)
                        if pct != pcttmp:
                            print "pct done: " + str(pct)
                            Lobotomy.plugin_pct(plugin, database, pct)
                    pcttmp = pct



    Lobotomy.plugin_pct(plugin, database, 50)
    print "pct done: " + str(50)
    # bereken md5 en sha1 hash over de files uit reports.log
    # exif info over de files
    Lobotomy.plugin_pct(plugin, database, 100)
    print "pct done: " + str(100)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
