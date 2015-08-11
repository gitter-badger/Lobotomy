__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.2
# 11 aug 2015:  WV
# Plugin:   memmap.


import sys
import commands
import main
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "memmap"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin

    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        print "Running Volatility - ", plugin, ", please wait."
        vollog = ""
        status, vollog = commands.getstatusoutput(command)

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing volatility output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing volatility output: " + plugin)

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(vollog)
        f.close()
    except:
        pass

    items = vollog.split('\n')
    print 'Parsing ' + plugin + ' data...'

    for line in items:
        if 'pid' in line:
            test = line.split(' ')
            name = test[0]
            pid = line[-1:]
        if line.startswith('Virtual'):
            pass # skip this line.
        if line.startswith('-----'):
            pass # skip this line.
        else:
            test = line.split(' ')
            virtual = ''
            physical = ''
            size = ''
            dumpfileoffset = ''
            save_sql = 0
            for data in test:
                if data.startswith('0x'):
                    # Save SQl before we overwrite things with new values
                    if size != '' and dumpfileoffset == '' and data.startswith('0x'):
                        dumpfileoffset = data
                        SQL_cmd = "INSERT INTO " + plugin + " VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}')".format\
                            (pid, name, virtual, physical, size, dumpfileoffset)
                        if DEBUG:
                            print SQL_cmd
                        else:
                            Lobotomy.exec_sql_query(SQL_cmd, database)
                    if physical != '' and size == '' and data.startswith('0x'):
                        size = data
                    if virtual != '' and physical == '' and data.startswith('0x'):
                        physical = data
                    if virtual == '' and data.startswith('0x'):
                        virtual = data

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
