__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# 16-03: WV - Netscan versie 0.1
#

import sys
import os
import main
from dateutil.parser import parse

Lobotomy = main.Lobotomy()
plugin = "netscan"

DEBUG = False


def main(database):
    Lobotomy.plugin_start('sockscan', database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    imagebit = imagetype[-2:]
    if DEBUG:
        print "\n\nImage = " + imagebit
    casedir = case_settings["directory"]
    if imagetype.startswith("WinXP"):
        print "Image not supprted!"
        exit()
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
                #Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
                #0x9a9cbf0          UDPv4    0.0.0.0:0                      *:*                                   1220     svchost.exe    2015-03-10 08:30:25 UTC+0000
                #0x9a9cbf0          UDPv6    :::0                           *:*                                   1220     svchost.exe    2015-03-10 08:30:25 UTC+0000
                #0xa7c9c40          UDPv4    10.10.3.228:138                *:*                                   4        System         2015-03-10 08:30:20 UTC+0000
                #0xa78e550          TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        916      svchost.exe
                #0xa78fac8          TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        916      svchost.exe
                #0xa78fac8          TCPv6    :::49154                       :::0                 LISTENING        916      svchost.exe
                if imagebit == '86':
                    if linestarts == 1:
                        offset = ''
                        proto = ''
                        localaddress = ''
                        foreignaddress = ''
                        state = ''
                        pid = ''
                        owner = ''
                        createtime = None
                        offset = line[0:19].strip(" ")
                        proto = line[19:25].strip(" ")
                        localaddress = line[28:59].strip(" ")
                        foreignaddress = line[59:80].strip(" ")
                        state = line[80:97].strip(" ")
                        pid = line[97:106].strip(" ")
                        owner = line[106:121].strip(" ").strip("\n")
#                        try:
                        createtime = line[121:140].strip("\n")
#                        except:
#                            createtime = 'NULL'
#                        print len(createtime)
                        if len(createtime) > 10:
                            createtime = parse(createtime).strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            createtime = 'NULL'
#                        if createtime is not None:
#                            createtime = parse(createtime).strftime("%Y-%m-%d %H:%M:%S")
#                        else:
#                            createtime = 'NULL'
                        SQL_cmd = "INSERT INTO " + plugin + " VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(offset, proto, localaddress, foreignaddress, state, pid, owner, createtime)
                        if DEBUG:
#                            print createtime
                            print SQL_cmd
                        else:
                            Lobotomy.exec_sql_query(SQL_cmd, database)

                    if line.startswith("Offset(P)"):
                        linestarts = 1
                if imagebit == 64:
                    print "Not yet implemented"
                    exit()

        linestarts = 0

    except IOError:
        print "IOError, file not found."
        if DEBUG:
            print "Debug mode is on: try creating a sample file."

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
    Lobotomy.plugin_stop(plugin, database)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
