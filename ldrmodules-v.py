__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "ldrmodules"

DEBUG = False

def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " -v"

    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
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
        print "Write log: " + database + " ,Stop: " + command
        print "Write log: " + casedir + " ,Stop: " + command
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start:  running plugin: " + plugin)

    try:
        f = open(imagename + '-' + plugin + '-v.txt', 'w')
        f.write(log)
        f.close()
    except:
        pass

    try:
        logcounter = 0
        for loglines in log.split('\n'):
            if folder in loglines:
                logcounter += 1
    except:
        pass

    items = log.split('\n')
    print 'Parsing ' + plugin + ' data...'

    lp = []
    Sql_cmd = ''
    loadpath = []
    mempath = []
    initpath = []
    writesql = []
    pid = 0
    tmpmem = 0
    tmpload = 0
    tmpinit = 0
    pidininit = ''
    pidinmem = ''
    pidinload = ''
    for line in items:
        #
        # Get the length of the columns
        #
        if line.startswith('-----'):
            lenline = line.split(' ')
            for item in lenline:
                lp.append(int(len(item) + 1))

        testpath = line.split(': ')
        if 'Load Path' in line:
            for item in testpath:
                if item != '':
                    item = item.strip(' ')
                    loadpath.append(item)
        if 'Init Path' in line:
            for item in testpath:
                if item != '':
                    item = item.strip(' ')
                    initpath.append(item)
        if 'Mem Path' in line:
            for item in testpath:
                if item != '':
                    item = item.strip(' ')
                    mempath.append(item)
        if pid == 1:
            if 'True' in pidinload and tmpload == 0:
                for item in loadpath:
                    writesql.append(item)
                    tmpload = 1
            if 'False' in pidinload and tmpload == 0:
                for tmp in range(3):
                    writesql.append('')
                    tmpload = 1
            if 'True' in pidininit and tmpinit == 0:
                for item in initpath:
                    writesql.append(item)
                    tmpinit = 1
            if 'False' in pidininit and tmpinit == 0:
                for tmp in range(3):
                    writesql.append('')
                    tmpinit = 1
            if 'True' in pidinmem and tmpmem == 0:
                for item in mempath:
                    writesql.append(item)
                    tmpmem = 1
            if 'False' in pidinmem and tmpmem == 0:
                for tmp in range(3):
                    writesql.append('')
                    tmpmem = 1

        if tmpload == 1 and tmpinit == 1 and tmpmem == 1 and pid == 1:
            Sql_cmd = ''
            Sql_prefix = "INSERT INTO ldrmodules_v VALUES (0,"
            for item in writesql:
                try:
                    item = item.replace('\\', '\\\\')
                except:
                    pass
                Sql_cmd = Sql_cmd + "'{}',".format(item)
            Sql_cmd = Sql_prefix + Sql_cmd[:-1] + ")"

            if DEBUG:
                print Sql_cmd
            else:
                Lobotomy.exec_sql_query(Sql_cmd, database)

            pidininit = ''
            pidinmem = ''
            pidinload = ''

            writesql = []
            mempath = []
            loadpath = []
            pid = 0
            tmpmem = 0
            tmpload = 0
            tmpinit = 0
            initpath = []

        try:
            if int(line[:8].strip(' ')):
                pidpid = int(line[:8].strip(' '))
                pidprocess = line[lp[0]:lp[0] + lp[1]].strip(' ')
                pidbase = line[lp[0]+lp[1]:lp[0]+lp[1]+lp[2]].strip(' ')
                pidinload = line[lp[0]+lp[1]+lp[2]:lp[0]+lp[1]+lp[2]+lp[3]].strip(' ')
                pidininit = line[lp[0]+lp[1]+lp[2]+lp[3]:lp[0]+lp[1]+lp[2]+lp[3]+lp[4]].strip(' ')
                pidinmem = line[lp[0]+lp[1]+lp[2]+lp[3]+lp[4]:lp[0]+lp[1]+lp[2]+lp[3]+lp[4]+lp[5]].strip(' ')
                pidpath = line[lp[0]+lp[1]+lp[2]+lp[3]+lp[4]+lp[5]:]

                writesql.append(int(line[:8].strip(' ')))
                writesql.append(line[lp[0]:lp[0] + lp[1]].strip(' '))
                writesql.append(line[lp[0]+lp[1]:lp[0]+lp[1]+lp[2]].strip(' '))
                writesql.append(line[lp[0]+lp[1]+lp[2]:lp[0]+lp[1]+lp[2]+lp[3]].strip(' '))
                writesql.append(line[lp[0]+lp[1]+lp[2]+lp[3]:lp[0]+lp[1]+lp[2]+lp[3]+lp[4]].strip(' '))
                writesql.append(line[lp[0]+lp[1]+lp[2]+lp[3]+lp[4]:lp[0]+lp[1]+lp[2]+lp[3]+lp[4]+lp[5]].strip(' '))
                writesql.append(line[lp[0]+lp[1]+lp[2]+lp[3]+lp[4]+lp[5]:])
                pid = 1
        except:
            pass

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop:  running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
