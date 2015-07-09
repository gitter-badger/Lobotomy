__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script.version    0.1
# Date:             09-07-2015
# Edited:           W Venhuizen
#

import sys
import commands
import main

Lobotomy = main.Lobotomy()
plugin = "yarascan"

DEBUG = False


def run_main(database, yararule):
    Lobotomy.plugin_start('volatility_' + plugin, database)
    Lobotomy.plugin_pct('volatility_' + plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]


    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + ' --yara-file=yara_rules/' + yararule
    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print command
    else:
        print "Running Volatility, plugin: " + plugin + ", please wait."
        log = ""
        status, log = commands.getstatusoutput(command)
    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    try:
        f = open(imagename + '-volatility_' + plugin + '.txt', 'w')
        f.write(log)
        f.close()
    except:
        pass

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing " + plugin + " output: " + 'volatility_' + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing " + plugin + " output: " + 'volatility_' + plugin)

    sql_prefix = "INSERT INTO volatility_" + plugin + " VALUES (0, "
    sql_line = ''
    counter = 0
    count = 0
    pct = 0
    blob = 0
    db_rule = ''
    db_owner = ''
    db_owner_name = ''
    db_pid = ''
    db_data_offset = ''
    db_data_bytes = ''
    db_data_txt = ''

    try:
        logcounter = 0
        for loglines in log.split('\n'):
            if folder in loglines:
                logcounter += 1
    except:
        pass

    lines = log.split('\n')
    print 'Parsing ' + 'volatility_' + plugin + ' data...'
    for line in lines:
        if not line.startswith('Volatility Foundation Volatility Framework'):
            try:
                pct = str(float(1.0 * count / logcounter) * 99).split(".")[0]
            except:
                pass
            count += 1

            if line.startswith('Rule:'):
                blob = 0
                try:
                    db_rule = line.split(' ', 1)[1]
                except:
                    pass
            if line.startswith('Owner:'):
                try:
                    db_owner = line.split(' ', 2)[1]
                except:
                    pass
            if line.startswith('Owner:'):
                blob = 1
                try:
                    db_owner_name = line.split(' Process ')[1].split(' Pid ')[0]
                except:
                    pass
            if line.startswith('Owner:'):
                try:
                    db_pid = line.split(' Pid ')[1]
                    blob = 1
                except:
                    pass

            if blob == 1 and imagetype[-3:] == 'x86' and not line.startswith('Owner'):
                try:
                    db_data_offset = db_data_offset + line.split(' ', 1)[0] + "\n"
                    db_data_bytes = db_data_bytes + line[12:60] + "\n"
                    db_data_txt = db_data_txt + line[62:79] + "\n"
                except:
                    pass

            if line.startswith('Rule:') and db_data_txt != '':
                sql_line = sql_prefix + "'{}', '{}', '{}', '{}', '{}', '{}', '{}'".\
                    format(
                    db_rule,
                    db_owner,
                    db_owner_name,
                    db_pid,
                    db_data_offset,
                    db_data_bytes,
                    db_data_txt + "')")[:-1]

                try:
                    Lobotomy.exec_sql_query(sql_line, database)
                    Lobotomy.plugin_pct('volatility_' + plugin, database, pct)
                except:
                    print 'Error sql query: ' + sql_line + " - " + database

                db_rule = ''
                db_owner = ''
                db_owner_name = ''
                db_pid = ''
                db_data_offset = ''
                db_data_bytes = ''
                db_data_txt = ''

    Lobotomy.plugin_stop('volatility_' + plugin, database)
    Lobotomy.plugin_pct('volatility_' + plugin, database, 100)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename> <yararule>"
    else:
        run_main(sys.argv[1], sys.argv[2])
