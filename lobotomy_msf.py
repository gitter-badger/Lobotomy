__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script version    0.5
# Plugin version:   0.1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           MSF Detect
# Edit:             13 okt 2015
# Detail:           Try to detect MSF exploit
# Detail:           Needed for Report function


import sys
import commands
import main
# from lobotomy_threatreport import
# threatreport = lobotomy_threatreport.Lobotomy()
Lobotomy = main.Lobotomy()

plugin = "msfdetect"

DEBUG = False


def main(database):
    command = []
    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database
    log = ''
    global pidlist
    pidlist = []

    command.append('strings -a -td {} | grep stdapi > {}/meterpreter_strings.txt'.format(imagename, casedir))
    command.append('vol.py -f {} --profile={} strings -s {}/meterpreter_strings.txt'.format(imagename, imagetype, casedir))

    # Lobotomy.write_to_main_log(database, " Start: " + command)
    # Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print command
    else:
        print "Running Lobotomy - {}, please wait.".format(plugin)
        for cmd in command:
            tmp = cmd.split(' ')
            print 'Running: {}'.format(tmp[0])
            log = ''
            status, log = commands.getstatusoutput(cmd)
    # Lobotomy.write_to_main_log(database, " Stop : " + command)
    # Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(log)
        f.close()
    except:
        pass

    get_msfstrings(log, database)

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)


def get_msfstrings(log, database):
    items = log.split('\n')
    print 'Parsing {} data...'.format(plugin)
    sql_list = []
    pidlist = []
    pids = ''
    for line in items:
        # try:
        if not line.startswith('Volatility Foundation Volatility'):
            stringsoffset = ''
            pid = 0
            pidoffset = ''
            vpid = 0
            vpidoffset = ''
            value = ''
            tmp = ''
            if '[FREE MEMORY]' in line:
                test = line.split('] ')[0].split('[')[1]
                # test for victim pid (infected pid)
                pids = line.split('[')[1].split(']')[0]
                if pids.count(':') > 1:
                    try:
                        vpid = pids.split(':')[1].split(' ')[1]
                        vpidoffset = pids.split(':')[2].split(' ')[0]
                    except:
                        pass
                pidoffset = test
                pid = 0
            if '[FREE MEMORY]' not in line:
                pids = line.split('[')[1].split(']')[0]
                pid = pids.split(':', 1)[0]
                pidoffset = pids.split(':', 1)[1].split(' ')[0]
                # test for victim pid (infected pid)
                if pids.count(':') > 1:
                    try:
                        vpid = pids.split(':')[1].split(' ')[1]
                        vpidoffset = pids.split(':')[2].split(' ')[0]
                    except:
                        pass
            stringsoffset = line.split(' ', 1)[0]
            value = line.split('] ')[1]
            value = value.replace('\\', '\\\\')
            value = value.replace("'", '"')
            sql_list.append([stringsoffset, pid, pidoffset, vpid, vpidoffset, value])

    for row in sql_list:
        sql_cmd = ''
        sql_cmd = "INSERT INTO {} VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}')".format(plugin,
                                                row[0], row[1], row[2], row[3], row[4], row[5])
        try:
            Lobotomy.exec_sql_query(sql_cmd, database)
        except:
            print 'SQL Error in ', database, 'plugin: ', plugin
            print 'SQL Error: ',  sql_cmd

    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
