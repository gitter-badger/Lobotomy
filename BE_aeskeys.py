__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.1
# Date:             05-05-2015
# Edited:           W Venhuizen
# Plugin:           Bulk Extractor - AESKeys
#

import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "BE_aes_keys"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    pct = 0

    Lobotomy.plugin_pct(plugin, database, 0)

    # Command niet nodig. Keys komen uit Bulk extractor.

    #command = "bulk_extractor -o " + dumpdir + " -e all " + imagename

    #command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + plugin + ".txt"
    
    #if DEBUG:
    #    print "Write log: " + database + ", Start: " + command
    #    print "Write log: " + casedir + ", Start: " + command
    #else:
    #    Lobotomy.write_to_main_log(database, " Start: " + command)
    #    Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    #if DEBUG:
    #    print command
    #else:
    #    os.system(command)

    Lobotomy.plugin_pct(plugin, database, 50)
        
    #if DEBUG:
    #    print "Write log: " + database + ", Stop: " + command
    #    print "Write log: " + casedir + ", Stop: " + command
    #else:
    #    Lobotomy.write_to_main_log(database, " Stop : " + command)
    #    Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start: running plugin: " + plugin)






    #with open(casedir + "/BE_dump/" + plugin + ".txt") as f:
    a = ""
    with open(casedir + "/BE_dump/aes_keys.txt") as f:
        for line in f:
            if not line.startswith('#'):
                #offset = line.strip(" ").split()[0]
                offset = line.split("\t")[0]
                type = line.split("\t")[-1].strip("\n")
                key = a.join(line.strip(" ").split("\t")[1:-1]).strip(" ")
                SQL_cmd = "INSERT INTO BE_aes_keys VALUES ('{}', '{}', '{}')".format(offset, key, type)
                if DEBUG:
                    print SQL_cmd
                else:
                    Lobotomy.exec_sql_query(SQL_cmd, database)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop: running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop: running plugin: " + plugin)
        Lobotomy.plugin_stop(plugin, database)

    Lobotomy.plugin_pct(plugin, database, 100)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
