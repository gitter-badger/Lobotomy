__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script.version    0.1
# Date:             06-07-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Eerste opzet yarascan voor lobotomy.
#

import sys
import main
import commands

Lobotomy = main.Lobotomy()
plugin = "Yarascan"

DEBUG = False


def main(database, folder):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]

    command = "yara yara_rules/index.yara " + folder + " -m -s"

    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print command
    else:
        print "Running yarascan on folder: " + folder
        log = ""
        status, log = commands.getstatusoutput(command)
    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing Yara output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing Yara output: " + plugin)

    try:
        logcounter = 0
        for loglines in log.split('\n'):
            if folder in loglines:
                logcounter += 1
    except:
        pass

    counter = 0
    count = 0
    b = ''
    c = ''
    sql_prefix = "INSERT INTO yarascan VALUES (0, "

    for item in log.split('\n'):
        try:
            pct = str(float(1.0 * count / logcounter) * 99).split(".")[0]
        except:
            pass
        if folder in item:
            count += 1
            counter += 1
            yara = item.split('[')[0]
            if 'description' in item:
                start = int(item.find('description')+13)
                yara_description = item[start:].split('"')[0]
                filename = "/" + item.split('/', 1)[1].replace('//', '/')
        else:
            a = item.split(':')
            try:
                offset = a[0]
            except:
                offset = ''
            try:
                description = a[1]
            except:
                description = ''
            try:
                string = a[2]
            except:
                string = ''
            try:
                sql_line = sql_prefix + "'{}', '{}', '{}', '{}', '{}', '{}'".format(filename, offset, description, \
                    string, yara, yara_description + "')")[:-1]
                Lobotomy.exec_sql_query(sql_line, database)
                Lobotomy.plugin_pct(plugin, database, pct)
                counter = 0
            except:
                print 'Error sql query: ' + sql_line + " - " + database
                counter = 0
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <database> <folder>"
    else:
        main(sys.argv[1], sys.argv[2])

