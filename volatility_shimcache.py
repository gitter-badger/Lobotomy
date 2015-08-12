__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# 12 aug 2015   WV
# Shimcache is voor Windows XP en Windows 7 anders.
# Een eigen plugin maken voor Shimcache.
#

import sys
import commands
import main
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "shimcache"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database

    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin

    Lobotomy.write_to_main_log(database, " Start: " + command)
    Lobotomy.write_to_case_log(casedir, " Start: " + command)
    if DEBUG:
        print command
    else:
        print "Running Volatility -", plugin, ", please wait."
        vollog = ""
        status, vollog = commands.getstatusoutput(command)
    Lobotomy.write_to_main_log(database, " Stop : " + command)
    Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(vollog)
        f.close()
    except:
        pass

    items = vollog.split('\n')
    print 'Parsing ' + plugin + ' data...'

    last_modified = ''
    last_update = ''
    path = ''
    columncount = 0
    for line in items:
        if not line.startswith('Last') and columncount != 0 and line != '':
            last_modified = line[0:len(test[0])]
            last_modified = parse(last_modified).strftime("%Y-%m-%d %H:%M:%S")
            if columncount == 2:
                path = line[len(test[0]) + 1:]
                last_update = ''
                sql_line = "INSERT INTO " + plugin + " VALUES ("
                sql_line = sql_line + "0, '{}', 0, '{}')".format\
                    (last_modified, path)
            if columncount == 3:
                last_update = line[len(test[0]) + 1:len(test[0]) + 1 + len(test[1])]
                last_update = parse(last_update).strftime("%Y-%m-%d %H:%M:%S")
                path = line[len(test[0]) + 1 + len(test[1]) +1:]
                print line[len(test[0]) + 1 + len(test[1]) +1:]
                sql_line = "INSERT INTO " + plugin + " VALUES ("
                sql_line = sql_line + "0, '{}', '{}', '{}')".format\
                    (last_modified, last_update, path)
            print last_modified, last_update, path
            print sql_line
            if DEBUG:
                print sql_line
            else:
                Lobotomy.exec_sql_query(sql_line, database)
        if line.startswith('----'):
            test = line.split(' ')
            for tmp in test:
                columncount += 1

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
