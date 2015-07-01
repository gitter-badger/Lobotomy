__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# 18-02: WV - Consoles versie 0.1, quick and dirty. Nog geen mogelijkheid om de consoles op een nette manier te parsen.
#


import sys
import os
import main
Lobotomy = main.Lobotomy()
plugin = "consoles"

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

    with open(imagename + "-" + plugin + ".txt") as f:
        for line in f:
            if not line.startswith("**************"):
                line = line.strip("\n")
                line = line.replace('\\', '\\\\')
                SQL_cmd = "INSERT INTO " + plugin + " VALUES (0, '{}')".format(line)
                Lobotomy.exec_sql_query(SQL_cmd, database)

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
