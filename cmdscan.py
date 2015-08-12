__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# 1902    Wv:     Aanpassen filenaam.
#
# 12 aug 2015   WV
# Werkend maken van de plugin.
#

import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "cmdscan"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database

    command = "vol.py -f " + imagename + " --profile=" + imagetype + " cmdscan"

    Lobotomy.write_to_main_log(database, " Start: " + command)
    Lobotomy.write_to_case_log(casedir, " Start: " + command)
    if DEBUG:
        print command
    else:
        print "Running Volatility - ", plugin, ", please wait."
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
    pid = ''
    CommandProcess = ''
    CommandHistory = ''
    Application = ''
    Flags = ''
    CommandCount = ''
    LastAdded = ''
    LastDisplayed = ''
    FirstCommand = ''
    CommandCountMax = ''
    ProcessHandle = ''
    cmd = ''

    for line in items:
        if line.startswith('*****'):
            pid = ''
            CommandProcess = ''
            CommandHistory = ''
            Application = ''
            Flags = ''
            CommandCount = ''
            LastAdded = ''
            LastDisplayed = ''
            FirstCommand = ''
            CommandCountMax = ''
            ProcessHandle = ''
            cmd = ''
        else:
            test = line.split(': ')
            if line.startswith('CommandProcess'):
                CommandProcess = test[1][:-4]
                pid = test[2]
            if line.startswith('CommandHistory'):
                CommandHistory = test[1].split(' ')[0]
                Application = test[2][:-6]
                Flags = test[-1]
            if line.startswith('CommandCount'):
                CommandCount = line.split(' ')[1]
                LastAdded = line.split(' ')[3]
                LastDisplayed = line.split(' ')[5]
            if line.startswith('FirstCommand'):
                FirstCommand = line.split(' ')[1]
                CommandCountMax  = line.split(' ')[3]
            if line.startswith('ProcessHandle'):
                ProcessHandle = test[1]
            if line.startswith('Cmd'):
                cmd = line
                sql_line = "INSERT INTO cmdscan VALUES ("
                sql_line = sql_line + "0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format\
                    (pid, CommandProcess, CommandHistory, Application, Flags, CommandCount, LastAdded, LastDisplayed,
                    FirstCommand, CommandCountMax, ProcessHandle, cmd)
                if DEBUG:
                    print sql_line
                else:
                    Lobotomy.exec_sql_query(sql_line, database)

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
