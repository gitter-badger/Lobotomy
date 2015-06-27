__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
### 19-02: WV - Geschikt gemaakt voor Windows 8.
###


import sys
import os
import main
Lobotomy = main.Lobotomy()

DEBUG = False


def main(database):
    Lobotomy.plugin_start('getsids', database)
    plugin = "getsids"
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + "-" + plugin + ".txt"
    
    Lobotomy.write_to_main_log(database, " Start: " + command)
    Lobotomy.write_to_case_log(casedir, " Start: " + command)
    if DEBUG:
        print command
    else:
        os.system(command)
    Lobotomy.write_to_main_log(database, " Stop : " + command)
    Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start:  running plugin: " + plugin)
    with open(imagename + "-" + plugin + ".txt") as f:
    
        for line in f:
            comment = ""
            a, b = line.split(":")
            proc, pid = a.split("(")
            try:
                sid, user = b.split("(")  # S-1-5-6 (Service), of S-1-2-0 (Local (Users ...))
                comment = " "
            except ValueError:
                try:
                    sid, user, comment = b.split("(")  # S-1-2-0 (Local (Users ...)) of S-1-5-90-0
                except ValueError:
                    sid = b.split("(")  # S-1-5-90-0
                    user = ""
                    comment = ""

            try:
                pid = pid.strip(")")
            except AttributeError:
                pass
            try:
                sid = sid.strip()
            except AttributeError:
                sid = sid[0].strip("\n")
            try:
                user = user.strip("\n").strip(")")
            except AttributeError:
                pass
            try:
                comment = comment.strip("\n").strip(")")
            except AttributeError:
                pass
            SQL_cmd = "INSERT INTO getsids VALUES (0, '{}', '{}', '{}', '{}', '{}')".format(proc, pid, sid, user, comment)
            if DEBUG:
                print SQL_cmd
            else:
                Lobotomy.exec_sql_query(SQL_cmd, database)
                Lobotomy.plugin_stop(plugin, database)
                Lobotomy.plugin_pct(plugin, database, 100)

    Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: getsids.py [databasename]"
    else:
        main(sys.argv[1])
