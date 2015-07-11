__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
### 19-02: WV - Kleine aanpassingen en een bug verholpen waardoor
###             Windows 7 niet goed ingelezen werd.
###
### 03-09: WV - Parsing is fout. rijen zijn 'verschoven'.
###
#
#   11-07: WV - plugin start/stop/pct gefixed.
#


import sys
import os
import main
from dateutil.parser import parse
Lobotomy = main.Lobotomy()
plugin = "pstree"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " -v > " + imagename + "-" + plugin + "-v.txt"

    
    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        os.system(command)
        
    if DEBUG:
        print "Write log: " + database + ", stop: " + command
        print "Write log: " + casedir + ", Stop: " + command
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start:  running plugin: " + plugin)
    
    a = 0
    dots = 0
    offset = 0
    name = 0
    pid = 0
    ppid = 0
    thrds = 0
    hnds = 0
    plugintime = 0
    audit = 0
    cmd = 0
    path = 0

    with open(imagename + "-" + plugin + "-v.txt") as f:
        for line in f:
            if " 0x" in line and sql_change == 1:
                SQL_cmd = "INSERT INTO pstree VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(dots, offset, name, pid, ppid, thrds, hnds, plugintime, audit, cmd, path)
                if DEBUG:
                    print SQL_cmd
                else:
                    Lobotomy.exec_sql_query(SQL_cmd, database)
                dots = 0
                offset = 0
                pid = 0
                ppid = 0
                name = 0
                thrds = 0
                hnds = 0
                plugintime = 0
                audit = 0
                cmd = 0
                path = 0

            sql_change = 0
            # split op spatie en tel aantal dots
            if 'path:' in line:
                path = line.split(":", 1)[1].replace('\\', '\\\\')
                path = path.strip("\n")
                sql_change = 1
            if 'cmd:' in line:
                cmd = line.split(":", 1)[1].replace('\\', '\\\\')
                cmd = cmd.strip("\n")
                sql_change = 1
            if 'audit:' in line:
                audit = line.split(":", 1)[1].replace('\\', '\\\\')
                audit = audit.strip("\n")
                sql_change = 1

            if " 0x" in line:
                try:
                    dots = len(line.split(" ")[0])
                except ValueError:
                    pass
                try:
                    offset, name = line.split(" ")[1].split(":")
                except ValueError:
                    pass
                try:
                    pid = line[52:58].strip(" ")
                except ValueError:
                    pass
                try:
                    ppid = line[59:64].strip(" ")
                except ValueError:
                    pass
                try:
                    thrds = line[65:72].strip(" ")
                except ValueError:
                    pass
                try:
                    hnds = line[73:79].strip(" ")
                except ValueError:
                    pass
                try:
                    plugintime = line[79:]
                except ValueError:
                    pass
                try:
                    plugintime = parse(plugintime).strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            try:
                a = int(hnds)
            except:
                hnds = 0

            #SQL_cmd = "INSERT INTO pstree VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(dots, offset, name, pid, ppid, thrds, hnds, plugintime, audit, cmd, path)
        # Save laatste regel.
        SQL_cmd = "INSERT INTO pstree VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(dots, offset, name, pid, ppid, thrds, hnds, plugintime, audit, cmd, path)
        if DEBUG:
            print SQL_cmd
        else:
            Lobotomy.exec_sql_query(SQL_cmd, database)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
