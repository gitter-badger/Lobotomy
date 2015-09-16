__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script version    0.5
# Plugin version:   1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           procdump
# Edit:             15 sep 2015
# Detail:           Change: Save volatility output in casefolder.


# \* fixme
# Command: python /srv/lobotomy/lob_scripts/dumpproc.py 1509161519_Win7x86_persistence2a03bb9bvmem
# Priority: 4
# -------------------------
# Running Volatility - Procdump, please wait.
# plugin: procdump - Database: 1509161519_Win7x86_persistence2a03bb9bvmem - pct done: 9
# Traceback (most recent call last):
#   File "/srv/lobotomy/lob_scripts/dumpproc.py", line 150, in <module>
#     main(sys.argv[1])
#   File "/srv/lobotomy/lob_scripts/dumpproc.py", line 124, in main
#     Lobotomy.exec_sql_query(sql_line, database)
#   File "/srv/lobotomy/lob_scripts/main.py", line 128, in exec_sql_query
#     cur.execute(query)
#   File "/usr/lib/python2.7/dist-packages/MySQLdb/cursors.py", line 174, in execute
#     self.errorhandler(self, exc, value)
#   File "/usr/lib/python2.7/dist-packages/MySQLdb/connections.py", line 36, in defaulterrorhandler
#     raise errorclass, errorvalue
# _mysql_exceptions.ProgrammingError: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'pkg_re','sources').run_script(',''volatility==2.4', 'vol.py')','0','','')' at line 1")


import sys
import main
import commands
Lobotomy = main.Lobotomy()
plugin = "procdump"

DEBUG = False
DEBUGvol = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/procdump"
    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " --dump-dir=" + dumpdir
    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUGvol:
        print command
    else:
        print "Running Volatility -", plugin, ", please wait."
        vollog = ""
        status, vollog = commands.getstatusoutput(command)
        
    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  Parsing volatility output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  Parsing volatility output: " + plugin)

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(vollog)
        f.close()
    except:
        pass

    counter = 0
    result = []
    part = []
    linePointer = 0
    lastLinePointer = 0
    pointers = []

    items = vollog.split('\n')
    print 'Parsing ' + plugin + ' data...'

    for line in items:
        if counter == 2:
            for x in line.split(' '):
                pointers.append(len(x)+1)
            pointers.pop(len(pointers)-1)
            pointers.append(255)
        if counter > 2:
            for x in range(len(pointers)): # Loop aantal kolommen
                item = pointers[x] 
                lastLinePointer += item
                part.append(line[linePointer:lastLinePointer].strip('\n').strip(' '))
                linePointer += item
            linePointer = 0
            lastLinePointer = 0
            if DEBUG:
                pass
            result.append(part)
        counter += 1
        part = []

    count = 0
    counter = len(result)
    for listitem in result:
        if DEBUG:
           print listitem
        else:
            count += 1
            pct = str(float(1.0 * count / counter) * 99).split(".")[0]

            sql_line = "INSERT INTO " + plugin + " VALUES (0, "
            for item in listitem:
                item = item.replace('\\', '\\\\')
                sql_line = sql_line + "'{}',".format(item)
                if item == listitem[3] and item.startswith("OK:"):
                    md5 = Lobotomy.md5Checksum(dumpdir + "/" + listitem[3].strip("OK: "))
                    md5filename = listitem[3].strip("OK: ")
                    fullfilename = dumpdir + "/" + listitem[3].strip("OK: ")

                    # Exiftool routine
                    # moved routine due to the msg: 'Error: PEB at ... is unavailable (possibly due to paging)'
                    try:
                        command = "exiftool " + fullfilename
                        status, log = commands.getstatusoutput(command)
                        exif_SQL_cmd = "INSERT INTO exifinfo VALUES (0, '{}', '{}')".format(fullfilename, log)
                        Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                    except:
                        print "Error parse-ing file: " + fullfilename
                        exif_SQL_cmd = "INSERT INTO exifinfo VALUES (0, '{}', '{}')".format(fullfilename, 'Parse error')
                        Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                        pass
                else:
                    md5 = "0"
                    md5filename = ''
                    fullfilename = ''
            sql_line = sql_line + "'" + md5 + "','" + md5filename + "','" + fullfilename + "')"
            Lobotomy.exec_sql_query(sql_line, database)

            try:
                if pct != pcttmp:
                    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)
                    Lobotomy.plugin_pct(plugin, database, pct)
            except:
                pass
            pcttmp = pct

    Lobotomy.plugin_pct(plugin, database, 100)
    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(100)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Parsing volatility output: " + plugin + ")"
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  Parsing volatility output: " + plugin)
        Lobotomy.plugin_stop(plugin, database)
        Lobotomy.plugin_pct(plugin, database, 100)

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
