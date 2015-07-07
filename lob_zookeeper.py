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

Lobotomy = main.Lobotomy()
plugin = "zookeeper"

DEBUG = False


def main(database, folder):
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
    command = "cd zookeeper && python ZooKeeper.py -t " + database + " -d " + folder
    print "Please wait..\nRunning Zookeeper script on folder: " + folder
    log = ""
    status, log = commands.getstatusoutput(command)
    counter = 0
    sql_prefix = "INSERT INTO pe_scan VALUES (0, "
    sql_line = ''
    items = log.split('\n')
    print 'Parsing Zookeeper data'
    for item in items:
        print type(item)
        if item.startswith('fullfilename'):
            fullfilename = item.split(' ', 1)[1]
        if item.startswith('pe_compiletime'):
            pe_compiletime = item.split(' ', 1)[1]
        if item.startswith('original_filename'):
            original_filename = item.split(' ', 1)[1]
        if item.startswith('pe_packer'):
            pe_packer = item.split(' ', 1)[1]
        if item.startswith('filetype'):
            filetype = item.split(' ', 1)[1]
        if item.startswith('pehash'):
            pehash = item.split(' ', 1)[1]
        if item.startswith('md5'):
            md5 = item.split(' ', 1)[1]
        if item.startswith('pe_language'):
            pe_language = item.split(' ', 1)[1]
        if item.startswith('pe_dll'):
            pe_dll = item.split(' ', 1)[1]
        if item.startswith('filename'):
            filename = item.split(' ', 1)[1]
        if item.startswith('sha'):
            sha = item.split(' ', 1)[1]
        if item.startswith('tag'):
            tag = item.split(' ', 1)[1]
        if item.startswith('filesize'):
            filesize = item.split(' ', 1)[1]
        if item.startswith('yara_results'):
            yara_results = item.split(' ', 1)[1]
        if counter == 1:
            sql_line = sql_prefix + "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'".\
                format(fullfilename, original_filename, pe_compiletime, pe_packer, filetype, pe_language, pe_dll,\
                filename, md5, sha, pehash, tag, filesize, yara_results)
        if item.startswith('*****'):
            counter = 1
            print sql_line
            sql_line = ''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <database> <filename>"
    else:
        main(sys.argv[1], sys.argv[2])

