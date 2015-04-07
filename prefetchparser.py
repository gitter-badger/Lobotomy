__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import main
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "prefetchparser"

DEBUG = False


def main(database):
    Lobotomy.plugin_start('prefetchparser', database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + "-" + plugin + ".txt"
    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        os.system(command)
        
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

    begin = 0
    prefetchfile = 0
    executiontime = 0
    times = 0
    size = 0
    with open(imagename + "-" + plugin + ".txt") as f:
        for line in f:
            #Prefetch file                              Execution Time               Times Size
            #------------------------------------------ ---------------------------- ----- --------
            #CMD.EXE-87B4001.PF                         2013-03-14 14:39:18 UTC+0000    22     8316
            #Prefetch file                              Execution Time               Times Size
            #------------------------------------------ ---------------------------- ----- --------
            #IEXPLORE.EXE-27122324.PF                   2012-11-28 03:05:24 UTC+0000     5    69882
            #WMIPRVSE.EXE-28F301A9.PF                   2012-11-28 02:58:44 UTC+0000     7    42622
            #LANMANWRK.EXE-12FB2801.PF                  2012-11-28 03:04:51 UTC+0000     1     7202
            #KERNELDRV.EXE-28DA9AD0.PF                  2012-11-28 03:04:59 UTC+0000     1     7724
            #WUAUCLT.EXE-399A8E72.PF                    2012-11-28 02:58:21 UTC+0000     6    49614
            #IPCONFIG.EXE-2395F30B.PF                   2012-11-28 03:05:28 UTC+0000    13    19530

            if begin == 1:
                prefetchfile = line.split(" ")[0]
                executiontime = line[44:72]
                executiontime = parse(executiontime).strftime("%Y-%m-%d %H:%M:%S")
                times = line[73:78].strip(" ")
                size = line[79:].strip(" ").strip("\n")            
                SQL_cmd = "INSERT INTO prefetchparser VALUES (0, '{}', '{}', '{}', '{}')".format(prefetchfile, executiontime, times, size)
                if DEBUG:
                    print SQL_cmd
                else:
                    #print SQL_cmd
                    Lobotomy.exec_sql_query(SQL_cmd, database)
            if line.startswith("-------"):
                begin = 1

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
        Lobotomy.plugin_stop('prefetchparser', database)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
