__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
#   1902    Wv:     Aanpassen filenaam.
#

import sys
import os
import main
Lobotomy = main.Lobotomy()

DEBUG = False


def main(database):
    Lobotomy.plugin_start('cmdscan', database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database

    command = "vol.py -f " + imagename + " --profile=" + imagetype + " cmdscan > " + imagename + "-cmdscan.txt"

    Lobotomy.write_to_main_log(database, " Start: " + command)
    Lobotomy.write_to_case_log(casedir, " Start: " + command)
    os.system(command)
    Lobotomy.write_to_main_log(database, " Stop : " + command)
    Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    firstline = 0
    cmdscanvar = []
    cmdscanvartotal = []
    cmdregel = []
    cmdfound = 0
    with open(imagename + "-cmdscan.txt") as f:
        for line in f:
            if line.startswith("**************"):
                if firstline != 0:
                    cmdscanvar.append("\n")
                    cmdscanvartotal.append(cmdscanvar)
                firstline += 1
                cmdscanvar = []
            else:
                line = line.strip("\n").split(" ")
                for x in line:
                    if x == "Cmd":
                        cmdscanvar.append(x)
                        cmdfound = 1
                    else:
                        cmdscanvar.append(x)
                        if cmdfound == 1 and x.startswith("Cmd"):
                            cmdfound = 0
        cmdscanvartotal.append(cmdscanvar)

        for regel in cmdscanvartotal:
            counter = 22
            for a in regel:

                if a == "Cmd":
                    tmp = " ".join(regel[0:22]) + " " + (regel[counter]) + " " + (regel[counter+1]) + " " + (regel[counter+2]) + " " + (regel[counter+3]) + " " + (regel[counter+4])
                    cmdregel.append(tmp.split(" "))
                    counter += 5

        for regel in cmdregel:
            SQL_cmd = "0, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}". \
                format(regel[3], regel[1], regel[5], regel[7], regel[9], regel[11], regel[13], regel[15], regel[17],
                       regel[19], regel[21], regel[22], regel[23], regel[24], regel[25], regel[26])
            input_sql(database, SQL_cmd)
    Lobotomy.plugin_stop('cmdscan', database)
    Lobotomy.plugin_pct(plugin, database, 100)


def input_sql(database, SQL_cmd):
    if DEBUG:
        print SQL_cmd
    else:
        Lobotomy.exec_sql_query("INSERT INTO cmdscan VALUES " + SQL_cmd, database)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: cmdscanvar.py [databasename]"
    else:
        main(sys.argv[1])
