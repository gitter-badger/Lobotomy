__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script.version    0.1
# Date:             05-05-2015
# Edited:           W Venhuizen
# Plugin:           BulkExtractor
#

# 05-05-2015: aanpassing van dumpdir van dump_bulk naar BE_dump
#
#
#
#

import sys
import os
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "BulkExtractor"

DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/BE_dump"
    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass

    #command = "bulk_extractor -o " + dumpdir + " -e all " + imagename   -e facebook - enable scanner facebook
    command = "bulk_extractor -o " + dumpdir + " -e all -x wordlist " + imagename

    print command
#command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " --dump-dir=" + dumpdir
    
    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start:  Running Bulk_Extractor: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  Running Bulk_Extractor: " + plugin)

    if DEBUG:
        print command
    else:
        log = ""
        status, log = commands.getstatusoutput(command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Stop:  Running Bulk_Extractor: " + plugin)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
