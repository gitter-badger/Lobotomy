__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script.version    0.1
# Date:             05-05-2015
# Edited:           W Venhuizen
# Plugin:
#

import sys
import os
import main
import main_test
import time
from dateutil.parser import parse

Lobotomy = main.Lobotomy()
lobtest = main_test.Lobotomy()
plugin = "test"


DEBUG = True


def main(database, filename):
    md5 = Lobotomy.md5Checksum(filename)
    filesha256, filemtime, fileatime, filectime, filesize = lobtest.sha256checksum(filename)
    print "md5: " + md5
    print "sha256: " + filesha256
    print "m-time: " + parse(time.ctime(filemtime)).strftime("%Y-%m-%d %H:%M:%S")
    print "a-time: " + parse(time.ctime(fileatime)).strftime("%Y-%m-%d %H:%M:%S")
    print "c-time: " + parse(time.ctime(filectime)).strftime("%Y-%m-%d %H:%M:%S")
    print "size: " + str(filesize)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1], sys.argv[2])
