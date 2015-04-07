#!/usr/bin/env python

""" DESCRIPTION """
__author__ = 'Jeroen'
__copyright__ = 'Copyright 2014, COP Team 1'
#
# Edit: Wim Venhuizen - File event handler: controleer of de file een binary is.
#


import os
import sys
sys.path.insert(0, '/home/solvent')
import main
import time
import commands
import pyinotify

Lobotomy = main.Lobotomy()


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        Lobotomy.write_to_main_log("DIRECTORY WATCHER", "New file detected: {}".format(event))
        time.sleep(3)
        command = "file " + event.pathname
        vollog = ""
        status, filelog = commands.getstatusoutput(command)
        status = "new file: " + event.pathname + " - filetype: " + filelog.split(":")[1]
        print status
        #if filelog.split(":")[1] == "data":
        if event.pathname[-4:] == '.exe':
            pass
        else:
            if event.pathname[-4:] != '.ini':
                dump = event.pathname
                dump = dump.split('/')
                dump = dump[-1]
                md5 = Lobotomy.md5Checksum(event.pathname)
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
                Lobotomy.write_to_main_log("DIRECTORY WATCHER", "Database created: {}".format(database))
                Lobotomy.exec_sql_query("UPDATE settings SET `md5hash`='{}'".format(md5), database)
                Lobotomy.write_to_main_log(database, "Database updated - md5hash={}".format(md5))
                Lobotomy.exec_sql_query("UPDATE settings SET `filename`='{}'".format(dump), database)
                Lobotomy.write_to_main_log(database, "Database updated - filename={}".format(dump))
                Lobotomy.exec_sql_query("UPDATE settings SET `directory`='{}'".format(random_dir), database)
                Lobotomy.write_to_main_log(database, "Database updated - directory={}".format(random_dir))
                Lobotomy.exec_sql_query("UPDATE settings SET `filepath`='{}'".format(random_dir + '/' + dump), database)
                Lobotomy.write_to_main_log(database, "Database updated - filepath={}".format(random_dir + '/' + dump))
                Lobotomy.exec_sql_query("UPDATE settings SET `initialized`=NOW()", database)
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
                else:
                    Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'imageinfo.py {}'.format(database), 1)
                Lobotomy.add_to_queue('python ' + Lobotomy.plugin_dir + 'autostart.py {}'.format(database))


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