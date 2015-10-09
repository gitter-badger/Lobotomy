__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script version    0.5
# Plugin version:   0.1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           Threads
# Edit:             14 sep 2015
# Detail:           Needed for Report function


import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "threads"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database

    command = 'vol.py -f {} --profile={} {}'.format(imagename, imagetype, plugin)

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
    print 'Parsing {} data...'.format(plugin)

    ethread = ''
    pid = ''
    tid = ''
    tags = ''
    created = ''
    exited = ''
    owner = ''
    state = ''
    sql_blob = ''
    sql_list = []
    for line in items:
        # skip the first lines
        if not line.startswith('Volatility Foundation Volatility') and not \
                line.startswith('[x86] Gathering all referenced SSDTs from KTHREADs...') and not \
                line.startswith('Finding appropriate address space for tables...'):
            if line.startswith('----'):
                # not me
                if state != '':
                    # write SQL
                    sql_list.append([ethread, pid, tid, tags, created, exited, owner, state, sql_blob])
                    ethread = ''
                    pid = ''
                    tid = ''
                    tags = ''
                    created = ''
                    exited = ''
                    owner = ''
                    state = ''
                    sql_blob = ''
            if line.startswith('ETHREAD:'):
                ethread = line.split(': ')[1].split(' ')[0]
                pid = line.split(': ')[2].split(' ')[0]
                tid = line.split(': ')[3]
            if line.startswith('Tags:'):
                tags = line.split(': ')[1]
            if line.startswith('Created:'):
                created = line.split(': ', 1)[1]
            if line.startswith('Exited: '):
                exited = line.split(': ', 1)[1]
            if line.startswith('Owning Process:'):
                owner = line.split(': ')[1]
            if line.startswith('State:'):
                state = line.split(': ')[1]
            if not line.startswith('----'):
                sql_blob += line + '\n'
                sql_blob = sql_blob.replace("'", '"')
    for row in sql_list:
        sql_cmd = ''
        sql_cmd = "INSERT INTO {} VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(plugin,
                                     row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        try:
            Lobotomy.exec_sql_query(sql_cmd, database)
        except:
            print 'SQL Error in ', database, 'plugin: ', plugin
            print 'SQL Error: ',  sql_cmd

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
