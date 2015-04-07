__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# 18-02: WV - Sockscan versie 0.1
#

import sys
import os
import main
from dateutil.parser import parse

Lobotomy = main.Lobotomy()
plugin = "sockscan"

DEBUG = False


def main(database):
    Lobotomy.plugin_start('sockscan', database)
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
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  running plugin: " + plugin)

    linestarts = 0
    mem = ""
    
    try:
        with open(imagename + "-" + plugin + ".txt") as f:
            for line in f:
                # solvent@lobotomy:~/dumps/4E16394GBVT8$ vol.py -f memfor3nov.vmem sockscan
                # Volatility Foundation Volatility Framework 2.4
                # Offset(P)       PID   Port  Proto Protocol        Address         Create Time
                # ---------- -------- ------ ------ --------------- --------------- -----------
                # 0x01da0240 152...53    836   8457 -               3.30.4.33       9194-03-30 18:09:33 UTC+0000
                # 0x01e48748        0   1280     32 MERIT-INP       0.5.0.0         -
                # 0x01e762d0     2276   1658     17 UDP             127.0.0.1       2013-03-14 14:19:34 UTC+0000
                # 0x01e854e8      180   2076      6 TCP             0.0.0.0         2013-03-14 14:40:18 UTC+0000
                # 0x01e8ae98     3832   1596      6 TCP             0.0.0.0         2013-03-14 14:18:39 UTC+0000
                # 0x01e8b440      180   1066      6 TCP             0.0.0.0         2013-03-14 03:03:13 UTC+0000
                # 0x01e8be98      180   1065      6 TCP             127.0.0.1       2013-03-14 03:03:13 UTC+0000
                # 0x01e9fcb0      180   2041      6 TCP             0.0.0.0         2013-03-14 14:39:28 UTC+0000
                # 0x01e9fe98      180   2060      6 TCP             0.0.0.0         2013-03-14 14:40:16 UTC+0000
                # 0x01eae638     1836   1203      6 TCP             127.0.0.1       2013-03-14 03:04:00 UTC+0000
                # 0x01eb28f8      180   2052      6 TCP             0.0.0.0         2013-03-14 14:39:28 UTC+0000
                # 0x01eb3310      180   2057      6 TCP             0.0.0.0         2013-03-14 14:40:16 UTC+0000
                # 0x01eb8008      180   2063      6 TCP             0.0.0.0         2013-03-14 14:40:17 UTC+0000
                # 0x01ee8008      180   2062      6 TCP             0.0.0.0         2013-03-14 14:40:17 UTC+0000
                # 0x01eeb1d8     3832   1594      6 TCP             0.0.0.0         2013-03-14 14:18:35 UTC+0000
                if linestarts == 1:
                    offset = line[0:10].strip(" ")
                    pid = line[11:19].strip(" ")
                    port = line[20:25].strip(" ")
                    proto = line[26:34].strip(" ")
                    protocol = line[34:49].strip(" ")
                    adress = line[50:66].strip(" ")
                    createtime = line[66:86]
                    createtime = parse(createtime).strftime("%Y-%m-%d %H:%M:%S")
                if linestarts == 1:
                    SQL_cmd = "INSERT INTO sockscan VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(offset, pid, port, proto, protocol, adress, createtime)
                    if DEBUG:
                        print SQL_cmd
                    else:
                        Lobotomy.exec_sql_query(SQL_cmd, database)
                if line.startswith("----------"):
                    linestarts = 1
        linestarts = 0

    except IOError:
        print "IOError, file not found."
        if DEBUG:
            print "Debug mode is on: try creating a sample file."

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
    Lobotomy.plugin_stop('sockscan', database)

    
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
