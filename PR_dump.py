__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.5
# Date:             05-05-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Edited:           W Venhuizen
# Parsing photorec logfile en bereken md5 over files.
# kleine aanpassing in console output. geen info is net te weinig als het lang duurt, voor screen maakt output niet uit.
#
# Date:             12-05-2015:
# Edited:           W Venhuizen
# kleine aanpassing in console output. Bij pct moet het processnaam staan. in de console staat nu alleen pct: ..
#
# Date:             17-05-2015:
# Edited:           W Venhuizen
# Aanpassing van de opgeslagen informatie. sha256 wordt berekend en de mac-time wordt opgeslagen.
#
# Date:             18-05-2015:
# Edited:           W Venhuizen
# Eerste poging exifinfo toe te voegen.
# Eerste volledige Testrun
# Stuxnet truncate op 255 tekens op kolom waarde, ophogen naar 512. aanpassen in (template) database.
# Error parse-ing file: /srv/lobotomy/dump/9XYG67O08Z3T/pr_dump.1/f0215056.exe
# Date:             09-07-2015:
# Edited:           W Venhuizen
# Plugin naam was fout opgegeven, waardoor in de tabel plugins niet de juiste waarde werdt gezet.
# Fix voor plugin end time
# Plugin Exifinfo meegenomen in de start-stop push naar de database.
# in voorkomend geval zou het kunnen zijn dat de tabel exifinfo niet zichtbaar is, omdat de waarde mist in tabel plugin.
# Date:             22 okt 2015:
# Edited:           W Venhuizen
# Detail:          Added: Check subprocess. If Exiftool takes longer then 60 seconds to run, kill it.
# Dependency:      subprocess, psutil and shlex

# \* fixme
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 21
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 22
# Error parse-ing file: /srv/lobotomy/dumps/JEFFY9YUQR4G/photorec_dump.1/f0183816.ttf
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 23
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 33
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 34
# sh: 1: Syntax error: "(" unexpected (expecting "}")
# sh: 1: Syntax error: "(" unexpected (expecting "}")
# sh: 1: Syntax error: "(" unexpected (expecting "}")
# plugin: photorec - Database: 1509170742_Bobvmem - pct done: 35

# Exifinfo dont need to check txt files and ttf?
# Or catch that error.

import sys
import os
import main
import time
import commands
import glob
from dateutil.parser import parse
import subprocess
import psutil
import shlex

Lobotomy = main.Lobotomy()
plugin = "photorec"

DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/photorec_dump"
    pct = 0
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_start('exifinfo', database)
    Lobotomy.plugin_pct(plugin, database, 0)

    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)

    try:
        log = ""
        status, log = commands.getstatusoutput("mkdir " + dumpdir)
        Lobotomy.write_to_main_log(database, " mkdir: " + log)
        Lobotomy.write_to_case_log(casedir, " mkdir: " + log)
    except:
        pass

    command = "photorec /debug /log /logname " + casedir + "/photorec.log /d " + dumpdir + " /cmd " + imagename + " fileopt,everything,enable,search"

    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Running: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start: Running: " + plugin)

    if DEBUG:
        print command
    else:
        print "Running photorec - Database: " + database + " - Please wait."
        log = ""
        status, log = commands.getstatusoutput(command)

    Lobotomy.plugin_pct(plugin, database, 5)
    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(5)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop: Running: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Stop: Running: " + plugin)

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop: Running: " + plugin + ")"
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop: Running: " + plugin)

    counter = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
            if line.startswith(casedir):
                filenaam = line.split("\t")[0]
                if not filenaam.endswith("mft") and filenaam.startswith(casedir):
                    counter += 1
    Lobotomy.plugin_pct(plugin, database, 10)
    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(10)
    print "Parsing " + plugin + " logfile"

    count = 0
    pcttmp = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
            try:
                if line.startswith(casedir):
                    filenaam = line.split("\t")[0]
                    filename = ''
                    filemd5 = ''
                    filesha256 = ''
                    mtime = ''
                    atime = ''
                    ctime = ''

                    #test of filenaam bestaat. mogelijke photorec bug.

                    if not filenaam.endswith("mft"):
                        if not os.path.isfile(filenaam):
                            tmp = len(filenaam.split("/")[-1])
                            tmpfilename = filenaam.split("/")[-1].split(".")[0]
                            tmpfilepath = filenaam[:-tmp]
                            filenaam = glob.glob(tmpfilepath + tmpfilename + "*")[0]

                        count += 1
                        try:
                            filemd5 = Lobotomy.md5Checksum(filenaam)
                        except:
                            filemd5 = ''
                            pass

                        try:
                            filesha256, filemtime, fileatime, filectime, filesize = Lobotomy.sha256checksum(filenaam)
                            mtime = parse(time.ctime(filemtime)).strftime("%Y-%m-%d %H:%M:%S")
                            atime = parse(time.ctime(fileatime)).strftime("%Y-%m-%d %H:%M:%S")
                            ctime = parse(time.ctime(filectime)).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            pass

                        pct = str(11 + (float(1.0 * count / counter) * 88)).split(".")[0]

                        filename = filenaam.split("/")[-1]

                        # Exiftool routine
                        command = "exiftool " + filenaam
                        args = shlex.split(command)
                        subp = subprocess.Popen(args, stdout=subprocess.PIPE)
                        p = psutil.Process(subp.pid)
                        log, err = subp.communicate()
                        try:
                            p.wait(timeout=60)
                        except psutil.TimeoutExpired:
                            p.kill()

                        try:
                            exif_SQL_cmd = "INSERT INTO exifinfo VALUES (0, '{}', '{}')".format(filenaam, log)
                            Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                        except:
                            print "Error parse-ing file: " + filenaam
                            exif_SQL_cmd = "INSERT INTO exifinfo VALUES (0, '{}', '{}')".format(filenaam, 'Parse error')
                            Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                            pass

                        try:
                            SQL_cmd = "INSERT INTO photorec VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".\
                                format(filenaam, filename, filemd5, filesha256, mtime, atime, ctime)
                        except:
                            pass #UnboundLocalError: local variable 'filemd5' referenced before assignment

                        try:
                            if DEBUG:
                                print SQL_cmd
                            else:
                                Lobotomy.exec_sql_query(SQL_cmd, database)
                                if pct != pcttmp:
                                    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)
                                    Lobotomy.plugin_pct(plugin, database, pct)
                        except:
                            pass
                        pcttmp = pct
            except IndexError:
                # IndexError: list index out of range
                pass

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_stop('exifinfo', database)
    Lobotomy.plugin_pct('exifinfo', database, 100)
    Lobotomy.plugin_pct(plugin, database, 100)
    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(100)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
