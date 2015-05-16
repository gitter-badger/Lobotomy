#!/usr/bin/env python

""" The main Lobotomy process """
__author__ = 'Jeroen Hagebeek, Wim Venhuizen'
__copyright__ = 'Copyright 2014, Fox Academy // Jeroen Hagebeek, Wim Venhuizen'

import os
import time
import string
import random
import hashlib
import MySQLdb
import MySQLdb.cursors
import datetime
from configobj import ConfigObj


class Lobotomy():
    def __init__(self):
        self.dump_dir = '/dumps/'  # Watch this directory for new memory dumps
        self.home_dir = '/home/solvent/'  # Home directory where queuefile will be placed
        self.copy_dir = '/home/solvent/dumps/'  # Copy processed memory dumps to this directory
        self.plugin_dir = '/home/solvent/lob_scripts/'  # Location of Lobotomy plugins
        self.mysql = ['localhost',  # Hostname
                      'root',  # Username
                      'Fwgs91VpfRRH22K',  # Password
                      'template']  # Database
        self.logfile = '/home/solvent/lobotomy.log'  # What logfile to use
        self.caselog = 'lobotomy.log'  # Filename to use for case log

    def write_to_main_log(self, database, message):
        """
        Write a message to the main logfile. The database name will be used as an identifier for the memory dump.
        :param database: The database of the memory dump
        :param message: The message to write to the log
        :return:
        """
        with open(self.logfile, "a") as log:
            now = datetime.datetime.now()
            entry = '{},{},{}\n'.format(now, database, message)
            log.write(entry)

    def write_to_case_log(self, casedir, message):
        """
        Write a message to the logfile in the memory dump's directory.
        :param casedir: The directory belonging to the memory dump
        :param message: The message to write to the log
        :return:
        """
        with open(casedir + '/' + self.caselog, "a") as log:
            now = datetime.datetime.now()
            entry = '{},{}\n'.format(now, message)
            log.write(entry)

    def add_to_queue(self, command, priority=3):
        """
        Add a command to the queue. Commands added to the queue will be executed automatically.
        Note: Enter a command as if you would on the command line, including 'python' if needed and using absolute paths
        :param command: The command to be executed
        :return:
        """
        self.exec_sql_query("INSERT INTO queue (command, priority, added) VALUES ('{}', {}, NOW())".format(command, priority), 'lobotomy')

    def read_from_queue(self):
        """
        Reads, and returns, the first line of the message queue and then removes that line
        :return: The line read
        """
        data = None
        sql = MySQLdb.connect(self.mysql[0], self.mysql[1], self.mysql[2], 'lobotomy',
                              cursorclass=MySQLdb.cursors.DictCursor)
        cur = sql.cursor()
        cur.execute("SELECT id, command, priority FROM queue ORDER BY priority ASC, id ASC LIMIT 1")
        data = cur.fetchone()
        if data is not None:
            cur.execute("INSERT INTO queue_archive SELECT q.*, NOW() FROM queue q WHERE id = {}".format(data['id']))
            sql.commit()
            cur.execute("DELETE FROM queue WHERE id={}".format(data['id']))
            sql.commit()
            return data
        else:
            return None

    def parse_cfg(self, ini):
        """
        Used to parse .ini files accompanying a memory dump.
        :param ini: The filename of the .ini file
        :return: A list with profile, comments, caseid and autostart as presented by the .ini file or 'None' for
                 absent fields
        """
        configfile = self.dump_dir + ini
        config = ConfigObj(configfile)
        try:
            profile = config['profile']
        except KeyError:
            profile = 'None'
        try:
            comments = config['comments']
        except KeyError:
            comments = 'None'
        try:
            autostart = config['autostart']
        except KeyError:
            autostart = 'No'
        try:
            caseid = config['caseid']
        except KeyError:
            caseid = 'None'
        os.remove(self.dump_dir + ini)
        return [profile, comments, caseid, autostart]

    @staticmethod
    def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def exec_sql_query(self, query, database):
        """
        Execute an SQL query for use with plugins, this way the individual plugins don't need to import mysqldb
        :param query: The query to be executed
        :param database: The database on which the query should be executed
        :return:
        """
        sql = MySQLdb.connect(self.mysql[0], self.mysql[1], self.mysql[2], database)
        cur = sql.cursor()
        cur.execute(query)
        sql.commit()
        sql.close()

    #def md5Checksum(self, filePath):
    #    with open(filePath, 'rb') as fh:
    #        m = hashlib.md5()
    #        while True:
    #            data = fh.read(8192)
    #            if not data:
    #                break
    #            m.update(data)
    #        return m.hexdigest()

    def md5Checksum(self, filePath):
        # Verify that the path is valid
        if os.path.exists(filepath):

            #Verify that the path is not a symbolic link
            if not os.path.islink(filepath):

                #Verify that the file is real
                if os.path.isfile(filepath):

                    try:
                        #Attempt to open the file
                        f = open(filepath, 'rb')
                    except IOError:
                        #if open fails report the error
                        print "\nOpen Failed " + filepath + "\n"
                        return

                    try:
                        with open(filePath, 'rb') as fh:
                            m = hashlib.md5()
                            while True:
                                data = fh.read(8192)
                                if not data:
                                    break
                                m.update(data)
                            return m.hexdigest()
                    except IOError:
                        # if read fails, then close the file and report error
                        f.close()
                        print "\nFile Read Error " + filepath +" \n"
                        return
                else:
                    print '[' + repr(simpleName) + ", Skipped Not a File" + ']'
                    return False
            else:
                print '[' + repr(simpleName) + ", Skipped Link Not a File" + ']'
                return False
        else:
            return False
            pass

    def sha256checksum(self, filepath):
        ONE_MB = 1024000  # 1 MB
        # Verify that the path is valid
        if os.path.exists(filepath):

            #Verify that the path is not a symbolic link
            if not os.path.islink(filepath):

                #Verify that the file is real
                if os.path.isfile(filepath):

                    try:
                        #Attempt to open the file
                        f = open(filepath, 'rb')
                    except IOError:
                        #if open fails report the error
                        print "\nOpen Failed " + filepath + "\n"
                        return

                    try:

                        # Hash the file
                        hash = hashlib.sha256()

                        # Attempt to read the file and hash the contents

                        rdBuffer = 'ok'

                        while len(rdBuffer):
                            rdBuffer = f.read(ONE_MB)
                            hash.update(rdBuffer)

                        #File processing completed
                        #Close the Active File
                        f.close()

                        # Once complete obtain the hex digest
                        hexOfHash = hash.hexdigest().upper()

                    except IOError:
                        # if read fails, then close the file and report error
                        f.close()
                        print "\nFile Read Error " + filepath +" \n"
                        return

                    #lets query the file stats

                    theFileStats = os.stat(filepath)
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filepath)

                    return hexOfHash, mtime, atime, ctime, size
                    #return True

                else:
                    print '[' + repr(simpleName) + ", Skipped Not a File" + ']'
                    return False
            else:
                print '[' + repr(simpleName) + ", Skipped Link Not a File" + ']'
                return False
        else:
            return False
            pass

    def create_database(self, dump):
        """
        Creates a database based on the filename of a memory dump and adds all required tables.
        The name will be in the format of "YYMMDDHHMM_filename" without dots.
        For example, a memory dump with the filename 'memorydump1.raw', picked up by the Directory Watcher on
                    05-12-2014 at 12:00 will be named 1412051200_memorydump1raw
        :param dump: The filename of the memory dump
        :return: The name of the newly created database
        """
        prefix = str(time.strftime("%y%m%d%H%M")) + '_'
        naam = prefix + dump
        naam = naam.replace('.', '')
        naam = naam.replace(' ', '')
        naam = naam.replace('-', '')
        sql = MySQLdb.connect(self.mysql[0], self.mysql[1], self.mysql[2])
        cur = sql.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;".format(naam))
        sql.commit()
        sql.close()
        return naam

    def populate_database(self, naam):
        print 'Populating database..'
        execute = "mysqldump -u {} -p{} template | mysql -u {} -p{} {}".format(self.mysql[1], self.mysql[2], self.mysql[1], self.mysql[2], naam)
        try:
            os.system(execute)
        except:
            print "------ ERROR while populating database! ------"
        finally:
            print 'Database populated!'

    def get_settings(self, database):
        """
        Returns a dictionary containing all values from the 'settings' table for the given database
        :param database: The name of the database from which to extract the settings. Returns a dictionary:
        :return: md5hash        varchar(32)
        :return: initialized    DATETIME
        :return: filename       varchar(255)
        :return: directory      varchar(255)
        :return: filepath       varchar(255)
        :return: caseid         INT
        :return: profile        varchar(255)
        :return: description    TEXT
        """
        sql = MySQLdb.connect(self.mysql[0], self.mysql[1], self.mysql[2], database,
                              cursorclass=MySQLdb.cursors.DictCursor)
        cur = sql.cursor()
        cur.execute("SELECT md5hash,initialized,filename,directory,filepath,caseid,profile,description FROM settings")
        settings = cur.fetchone()
        sql.close()
        return settings

    def plugin_start(self, plugin, database):
        self.exec_sql_query("UPDATE plugins SET started=NOW(), `status`=2 WHERE `name`='{}'".format(plugin), database)

    def plugin_stop(self, plugin, database):
        self.exec_sql_query("UPDATE plugins SET stopped=NOW(), `status`=1 WHERE `name`='{}'".format(plugin), database)

    def plugin_pct(self, plugin, database, pct):
        self.exec_sql_query("UPDATE plugins SET pct={} WHERE name='{}'".format(pct, plugin), database)