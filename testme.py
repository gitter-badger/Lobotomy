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
Lobotomy = main.Lobotomy()
lobtest = main_test.Lobotomy()
plugin = "test"


DEBUG = True


def main(database, filename):
    md5 = Lobotomy.md5Checksum(filename)
    filesha256, filemtime, fileatime, filectime, filesize = lobtest.sha256checksum(filename)
    print "md5: " + md5
    print "sha256: " + filesha256
    print "m-time: " + time.ctime(filemtime)
    print "a-time: " + time.ctime(fileatime)
    print "c-time: " + time.ctime(filectime)
    print "size: " + str(filesize)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1], sys.argv[2])
