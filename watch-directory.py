#!/usr/bin/env python

""" DESCRIPTION """
__author__ = 'Jeroen Hagebeek, Wim Venhuizen'
__copyright__ = 'Copyright 2014, Fox Academy // Jeroen Hagebeek, Wim Venhuizen'

#
# Script.version    0.1
# Date:             05-05-2015
# Edited:           W Venhuizen
# Plugin:
#
# Edit:             Wim Venhuizen - File event handler: controleer of de file een binary is.
#
# edit:             15-05-2015
# added sha256 and mac-time to the database
#




import os
import sys
import main
import time
import commands
import pyinotify
from dateutil.parser import parse

sys.path.insert(0, '/home/solvent')
DEBUG = False

Lobotomy = main.Lobotomy()

"""
Returns a dictionary containing all values from the 'settings' table for the given database
:param database: The name of the database from which to extract the settings. Returns a dictionary:
:return: md5hash        md5 hash
:return: initialized    time.strftime("%Y-%m-%d %H:%M:%S")
:return: filename       dump
:return: directory      random_dir
:return: filepath       random_dir + '/' + dump
:return: caseid         0
:return: profile        0
:return: description    0
:return: filesha256     sha256 hash
:return: mtime          Mac-time
:return: atime          mAc-time
:return: ctime          maC-time
"""

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        try:
            Lobotomy.write_to_main_log("DIRECTORY WATCHER", "New file detected: {}".format(event))
            time.sleep(3)
            command = "file " + event.pathname
            vollog = ""
            status, filelog = commands.getstatusoutput(command)
            status = "new file: " + event.pathname + " - filetype: " + filelog.split(":")[1]
            print status
            #if filelog.split(":")[1] == "data":
            #if event.pathname[-4:] == '.exe':
            #    pass
            #else:
            #    if event.pathname[-4:] != '.ini':
            dump = event.pathname
            dump = dump.split('/')
            dump = dump[-1]
            md5 = Lobotomy.md5Checksum(event.pathname)
            print md5
            filesha256, filemtime, fileatime, filectime, filesize = Lobotomy.sha256checksum(event.pathname)
            mtime = parse(time.ctime(filemtime)).strftime("%Y-%m-%d %H:%M:%S")
            atime = parse(time.ctime(fileatime)).strftime("%Y-%m-%d %H:%M:%S")
            ctime = parse(time.ctime(filectime)).strftime("%Y-%m-%d %H:%M:%S")
            print filesha256
            Lobotomy.write_to_main_log("DIRECTORY WATCHER", "Calculated {} MD5: {}".format(dump, md5))
            random_string = Lobotomy.id_generator()
            random_dir = Lobotomy.copy_dir + random_string
            print "mkdir", random_dir
            os.mkdir(random_dir)
            Lobotomy.write_to_main_log("DIRECTORY WATCHER", "Random directory created: {}".format(random_dir))
            new_file = random_dir + '/' + dump
            print "rename", Lobotomy.dump_dir + dump, new_file
            os.rename(Lobotomy.dump_dir + dump, new_file)
            Lobotomy.write_to_main_log("DIRECTORY WATCHER", "File {} moved to {}".format(Lobotomy.dump_dir + dump, random_dir + '/' + dump))
            profile = comments = case_id = autostart = 'None'
            tmp = dump.split('.')
            tmp[-1] = 'ini'
            ini = ".".join(tmp)
            database = Lobotomy.create_database(dump)
            Lobotomy.populate_database(database)
            print "database"

            SQL_cmd = "INSERT INTO settings VALUES " \
                      "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format\
                (md5, time.strftime("%Y-%m-%d %H:%M:%S"), dump, random_dir, random_dir + '/' + dump, 0, 0, 0, filesha256, mtime, atime, ctime)
            if DEBUG:
                print SQL_cmd
            else:
                Lobotomy.exec_sql_query(SQL_cmd, database)

                    #Lobotomy.write_to_main_log("DIRECTORY WATCHER", "Database created: {}".format(database))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `md5hash`='{}'".format(md5), database)
                    #Lobotomy.write_to_main_log(database, "Database updated - md5hash={}".format(md5))
                    #Lobotomy.write_to_main_log(database, "Database updated - mactime from memdump".format(mtime))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `filename`='{}'".format(dump), database)
                    #Lobotomy.write_to_main_log(database, "Database updated - filename={}".format(dump))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `directory`='{}'".format(random_dir), database)
                    #Lobotomy.write_to_main_log(database, "Database updated - directory={}".format(random_dir))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `filepath`='{}'".format(random_dir + '/' + dump), database)
                    #Lobotomy.write_to_main_log(database, "Database updated - filepath={}".format(random_dir + '/' + dump))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `initialized`=NOW()", database)
                    #Lobotomy.exec_sql_query("UPDATE settings SET `sha256hash`='{}'".format(filesha256), database)
                    #Lobotomy.write_to_main_log(database, "Database updated - sha256hash={}".format(filesha256))
                    #Lobotomy.exec_sql_query("UPDATE settings SET `mtime`='{}'".format(mtime), database)
                    #Lobotomy.exec_sql_query("UPDATE settings SET `atime`='{}'".format(atime), database)
                    #Lobotomy.exec_sql_query("UPDATE settings SET `ctime`='{}'".format(ctime), database)
            Lobotomy.write_to_main_log(database, "Database updated - initialized=NOW() -- MySQL function NOW() inserts the current timestamp".format(database))
            Lobotomy.exec_sql_query("INSERT INTO dumps (location, dbase, added, case_assigned) VALUES ('{}', '{}', NOW(), 0)".format(new_file, database), "lobotomy")
            if os.path.isfile(Lobotomy.dump_dir + ini):
                print "INI file found!", ini
                Lobotomy.write_to_main_log(database, "Found matching .ini file")
                profile, comments, case_id, autostart = Lobotomy.parse_cfg(ini)
                        # DEBUG:
                autostart = 1

                print profile, comments, case_id, autostart
                if profile is 'None':
                    Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'imageinfo.py {}'.format(database), 1)
                else:
                    Lobotomy.exec_sql_query("UPDATE settings SET `profile`='{}'".format(profile), database)
                    Lobotomy.write_to_main_log(database, "Database updated - profile={}".format(profile))
                    print "Database update. profile={}".format(profile)
                if autostart is 'yes' or 1 or '1':
                    Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'autostart.py {}'.format(database), 2)
                    Lobotomy.write_to_main_log(database, "Auto-start enabled")
                print "Database update. description={}".format(comments)
                if case_id is 'None':
                    Lobotomy.exec_sql_query("UPDATE settings SET caseid=0", database)
                    Lobotomy.write_to_main_log(database, "Database updated - caseid=0".format(database))
                    print "Database update. caseid=0"
                else:
                    Lobotomy.exec_sql_query("UPDATE settings SET caseid={}".format(case_id), database)
                    Lobotomy.write_to_main_log(database, "Database updated - caseid={}".format(case_id))
                    print "Database update. caseid={}".format(case_id)
            #else:
            #    Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'imageinfo.py {}'.format(database), 1)
            Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'autostart.py {}'.format(database))
        #except:
            #pass

def _main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('/dumps', pyinotify.IN_CLOSE_WRITE, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    _main()