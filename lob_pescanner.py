__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# Script version    0.5
# Plugin version:   1.1
# Plugin:           Lobotomy PE Scanner
# Date:             06-07-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Eerste opzet PE_Scanner voor lobotomy.
#
# 02 sep 2015:      Wim Venhuizen
#  Detail:          Fixed: An issue where the scripts try's to write a wrong sql query.
#                   there can sometimes a ' in the text.
#                   Change: Add plugin name in output.
# 22 okt 2015:      Wim Venhuizen
#  Detail:          Added: Check subprocess. If PEScanner takes longer then 60 seconds to run, kill it.
#  Dependency:      subprocess, psutil and shlex


import os
import sys
import main
import subprocess
import psutil
import time
import shlex

Lobotomy = main.Lobotomy()
plugin = "pescanner"

DEBUG = False


def main(database, folder):
    Lobotomy.plugin_start('pe_scanner_beta', database)
    #Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct('pe_scanner_beta', database, 1)
    #Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    sql_prefix = "INSERT INTO pe_scanner_beta VALUES (0, "
    counter = 0
    count = 0
    log = ''
    subp = ''
    pct = 0
    if folder == '':

        for subdir, dirs, files in os.walk(casedir):
            for folders in dirs:
                for subdir1, dirs1, files1 in os.walk(subdir + '/' + folders):
                    for loopfile in files1:
                        loopfilenaam = os.path.join(subdir1, loopfile)
                        if not loopfilenaam.endswith('.txt'):
                            counter += 1

        for subdir, dirs, files in os.walk(casedir):
            for folders in dirs:
                for subdir1, dirs1, files1 in os.walk(subdir + '/' + folders):
                    for loopfile in files1:
                        loopfilenaam = os.path.join(subdir1, loopfile)
                        if not loopfilenaam.endswith('.txt'):
                            count += 1
                            command = "python mcb_pescanner1.py " + loopfilenaam

                            args = shlex.split(command)
                            subp = subprocess.Popen(args, stdout=subprocess.PIPE)
                            p = psutil.Process(subp.pid)
                            log, err = subp.communicate()
                            try:
                                p.wait(timeout=60)
                            except psutil.TimeoutExpired:
                                p.kill()

                            try:
                                pct = str(float(1.0 * count / counter) * 99).split(".")[0]
                                print "Lobotomy PEScanner - Percentage done: ", pct
                            except:
                                pass
                            print "Lobotomy PEScanner - files to go: " + str(counter) + " from " + str(count)
                            print "Lobotomy PEScanner - Current filename: ", loopfilenaam
                            if log != '':
                                log = log.replace("'", '"').replace("`", "\`").replace('"', '\\"')
                                sql_line = sql_prefix + "'{}', '{}''".format(loopfilenaam, log + "')")[:-2]
                                try:
                                    Lobotomy.exec_sql_query(sql_line, database)
                                except:
                                    print sql_line
                                    #Lobotomy.exec_sql_query(sql_line, database)
                                Lobotomy.plugin_pct('pe_scanner_beta', database, pct)
                                #Lobotomy.plugin_pct(plugin, database, pct)

    Lobotomy.plugin_stop('pe_scanner_beta', database)
    Lobotomy.plugin_pct('pe_scanner_beta', database, 100)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: " + plugin + ".py <database> <folder>"
    else:
        folder = ''
        try:
            folder = sys.argv[2]
        except:
            pass
        main(sys.argv[1], folder)

