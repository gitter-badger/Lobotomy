__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# 27-06: WV -   Initiele aanmaak hashdump.
#               kijken of later de hash naar john gepast kan worden als hash cracker.


import sys
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "hashdump"

DEBUG = False


def main(database):
    Lobotomy.plugin_start('hashdump', database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]

    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass
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

    vollog = vollog.split("\n")
    for line in vollog:
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
                Lobotomy.plugin_pct(plugin, database, 100)
            except:
                print 'Error sql query: ' + sql_line + " - " + database

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
