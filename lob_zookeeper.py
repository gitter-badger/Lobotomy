__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script.version    0.1
# Date:             06-07-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Eerste opzet om zookeeper te gebruiken binnen lobotomy.
# Letop: De scripts van Zookeeper zijn aangepast voor de werking van lobotomy.
#

import sys
import main
import commands
import main
import time

Lobotomy = main.Lobotomy()
plugin = "pe_scan"

DEBUG = False


def main(database, folder):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]


    command = "cd zookeeper && python ZooKeeper.py -t " + database + " -d " + folder
    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    fullfilename = ''
    pe_compiletime = ''
    original_filename = ''
    pe_packer = ''
    filetype = ''
    pehash = ''
    md5 = ''
    pe_language = ''
    pe_dll = ''
    filename = ''
    sha = ''
    tag = ''
    filesize = ''
    yara_results = ''

    if DEBUG:
        print command
    else:
        print "Running ZooKeeper, please wait."
        log = ""
        status, log = commands.getstatusoutput(command)
    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing ZooKeeper output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing ZooKeeper output: " + plugin)


    sql_prefix = "INSERT INTO pe_scan VALUES (0, "
    sql_line = ''
    try:
        f = open(imagename + '-zookeeperlog.txt', 'w')
        f.write(log)
        f.close()
    except:
        pass
    items = log.split('\n')
    print 'Parsing Zookeeper data'
    for item in items:
        if item.startswith('fullfilename'):
            try:
                fullfilename = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('pe_compiletime'):
            try:
                pe_compiletime = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('original_filename'):
            try:
                original_filename = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('pe_packer'):
            try:
                pe_packer = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('filetype'):
            try:
                filetype = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('pehash'):
            try:
                pehash = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('md5'):
            try:
                md5 = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('pe_language'):
            try:
                pe_language = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('pe_dll'):
            try:
                pe_dll = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('filename'):
            try:
             filename = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('sha'):
            try:
                sha = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('tag'):
            try:
                tag = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('filesize'):
            try:
                filesize = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('yara_results'):
            try:
                yara_results = item.split(' ', 1)[1]
            except:
                pass
        if item.startswith('*****'):

            sql_line = sql_prefix + "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'".\
                format(fullfilename, original_filename, pe_compiletime, pe_packer, filetype, pe_language, pe_dll,
                       filename, md5, sha, pehash, tag, filesize, yara_results + "')")[:-1]
            try:
                #time.sleep(0.1)
                Lobotomy.exec_sql_query(sql_line, database)
                fullfilename = ''
                pe_compiletime = ''
                original_filename = ''
                pe_packer = ''
                filetype = ''
                pehash = ''
                md5 = ''
                pe_language = ''
                pe_dll = ''
                filename = ''
                sha = ''
                tag = ''
                filesize = ''
                yara_results = ''
            except:
                print 'Error sql query: ' + sql_line + " - " + database
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <database> <filename>"
    else:
        main(sys.argv[1], sys.argv[2])
