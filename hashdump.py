__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# Script version    0.6
# Plugin version:   1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           hashdump
# Edit:             15 sep 2015
# Detail:           Change: Save volatility output in casefolder.
#
# Edit:             27 jun 2015
# Detail:           Initiele aanmaak hashdump.
#                   kijken of later de hash naar john gepast kan worden als hash cracker.

# *\ fixme
# Command: python /srv/lobotomy/lob_scripts/hashdump.py 1509161519_Win7x86_persistence2a03bb9bvmem
# Priority: 4
# -------------------------
# Running Volatility - hashdump, please wait.
# Error sql query: INSERT INTO hashdump VALUES (0, 'ERROR   : volatility.plugins.registry.lsadump: Unable to read hashes from registry','ERROR   ',' volatility.plugins.registry.lsadump',' Unable to read hashes from registry') - 1509161519_Win7x86_persistence2a03bb9bvmem
# ID: 697


import sys
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "hashdump"

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
        print "Running Volatility - hashdump, please wait."
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
        sql_line = "INSERT INTO " + plugin + " VALUES (0, "
        if not line.startswith('Volatility Foundation Volatility Framework'):
            resultline = line.split(':')
            sql_line = sql_line + "'{}',".format(line)
            for result in resultline:
                if result != "":
                    sql_line = sql_line + "'{}',".format(result)
            sql_line = sql_line[:-1] + ")"
            try:
                Lobotomy.exec_sql_query(sql_line, database)
            except:
                print 'Error sql query: ' + sql_line + " - " + database
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
