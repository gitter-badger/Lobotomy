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
# aanpassing in except. gegevens toch proberen op te nemen in de database

import sys
import os
import main
import time
import commands
import glob
from dateutil.parser import parse

Lobotomy = main.Lobotomy()
plugin = "PhotoRec"

DEBUG = False

def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    dumpdir = casedir + "/pr_dump"
    pct = 0

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
        print "Write log: (" + casedir + ", Database: " + database + " Start:  Running PhotoRec: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  Running PhotoRec: " + plugin)

    if DEBUG:
        print command
    else:
        print "Running Photorec - database: " + database + ". Please wait."
        log = ""
        status, log = commands.getstatusoutput(command)

    Lobotomy.plugin_pct(plugin, database, 25)
    print "Plugin: " + plugin + " - Database: " + database + " - pct done: " + str(25)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running PhotoRec: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Stop:  Running PhotoRec: " + plugin)

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)
    
    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Stop:  Running PhotoRec: " + plugin + ")"
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  Running PhotoRec: " + plugin)

    counter = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
            if line.startswith(casedir):
                filenaam = line.split("\t")[0]
                if not filenaam.endswith("mft"):
                    counter += 1
    Lobotomy.plugin_pct(plugin, database, 30)
    print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(30)
    print "Parsing Photorec logfile"

    count = 0
    pcttmp = 0
    with open(casedir + "/photorec.log") as f:
        for line in f:
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
                        pass
                    try:
                        filesha256, filemtime, fileatime, filectime, filesize = Lobotomy.sha256checksum(filenaam)
                        mtime = parse(time.ctime(filemtime)).strftime("%Y-%m-%d %H:%M:%S")
                        atime = parse(time.ctime(fileatime)).strftime("%Y-%m-%d %H:%M:%S")
                        ctime = parse(time.ctime(filectime)).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass

                    pct = str(31 + (float(1.0 * count / counter) * 70)).split(".")[0]

                    filename = filenaam.split("/")[-1]

                    # Run Exiftool over de gevonden bestanden

                    try:
                        command = "exiftool " + filenaam
                        status, log = commands.getstatusoutput(command)
                        exiflog = log.split("\n")
                        for exifregel in exiflog:
                            omschrijving = exifregel.split(':')[0]
                            waarde = exifregel.split(':')[1][1:]
                            exif_SQL_cmd = "INSERT INTO exiffileinfo VALUES (0, '{}', '{}', '{}')".format(filenaam, omschrijving, waarde)
                            Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                    except:
                        print "Error parse-ing file: " + filenaam
                        exif_SQL_cmd = "INSERT INTO exiffileinfo VALUES (0, '{}', '{}', '{}')".format(filenaam, 'Error parse-ing file', log)
                        Lobotomy.exec_sql_query(exif_SQL_cmd, database)
                        pass

                    try:
                        SQL_cmd = "INSERT INTO PR_files VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(filenaam, filename, filemd5, filesha256, mtime, atime, ctime)
                    except:
                        pass #UnboundLocalError: local variable 'filemd5' referenced before assignment

                    try:
                        if DEBUG:
                            print SQL_cmd
                        else:
                            Lobotomy.exec_sql_query(SQL_cmd, database)
                            if pct != pcttmp:
                                print "Plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)
                                Lobotomy.plugin_pct(plugin, database, pct)
                    except:
                        pass
                    pcttmp = pct

    Lobotomy.plugin_pct(plugin, database, 100)
    print "Plugin: " + plugin + " - Database: " + database + " - pct done: " + str(100)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
