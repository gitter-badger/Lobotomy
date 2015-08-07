__author__ = 'Wim Venhuizen'

#
# Script.version    0.1
# Date:             08-03-2015
# Edited:           W Venhuizen
#
# Eerste opzet om bad_hashes op te halen van virusshare
#

import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()

starttime = time.time()
hashcount = 0

# -rw-rw-r--  1 solvent solvent 4325574 Jul  9  2014 VirusShare_00135.md5
# -rw-rw-r--  1 solvent solvent 4325574 Jul 29  2014 VirusShare_00136.md5
# -rw-rw-r--  1 solvent solvent 4325574 Jul 29  2014 VirusShare_00137.md5
# -rw-rw-r--  1 solvent solvent 4325574 Sep 24  2014 VirusShare_00138.md5
# -rw-rw-r--  1 solvent solvent 4325574 Sep 24  2014 VirusShare_00139.md5
# -rw-rw-r--  1 solvent solvent 4325574 Oct 31  2014 VirusShare_00140.md5
# -rw-rw-r--  1 solvent solvent 4325574 Oct 31  2014 VirusShare_00141.md5
# -rw-rw-r--  1 solvent solvent 4325574 Oct 31  2014 VirusShare_00142.md5
# -rw-rw-r--  1 solvent solvent 4325574 Nov  4  2014 VirusShare_00143.md5
# -rw-rw-r--  1 solvent solvent 4325574 Nov 27  2014 VirusShare_00144.md5
# -rw-rw-r--  1 solvent solvent 4325574 Dec 10  2014 VirusShare_00145.md5
# -rw-rw-r--  1 solvent solvent 4325574 Jan  5  2015 VirusShare_00146.md5
# -rw-rw-r--  1 solvent solvent 4325574 Jan 16  2015 VirusShare_00147.md5
# -rw-rw-r--  1 solvent solvent 4325574 Feb  6 04:17 VirusShare_00148.md5
# -rw-rw-r--  1 solvent solvent 2162886 Feb 19 04:25 VirusShare_00149.md5
# -rw-rw-r--  1 solvent solvent 2162886 Mar 20 02:56 VirusShare_00150.md5
# -rw-rw-r--  1 solvent solvent 2162886 Apr 17 03:18 VirusShare_00151.md5
# -rw-rw-r--  1 solvent solvent 2162886 Apr 17 03:18 VirusShare_00152.md5
# -rw-rw-r--  1 solvent solvent 2162886 May  9 23:08 VirusShare_00153.md5
# -rw-rw-r--  1 solvent solvent 2162886 May 12 16:34 VirusShare_00154.md5
# -rw-rw-r--  1 solvent solvent 2162886 May 30 20:53 VirusShare_00155.md5
# -rw-rw-r--  1 solvent solvent 2162886 May 30 20:54 VirusShare_00156.md5
# -rw-rw-r--  1 solvent solvent 2162886 Jun 19 05:12 VirusShare_00157.md5
# -rw-rw-r--  1 solvent solvent 2162886 Jun 30 04:09 VirusShare_00158.md5
# -rw-rw-r--  1 solvent solvent 2162886 Jul 25 04:44 VirusShare_00159.md5
# -rw-rw-r--  1 solvent solvent 2162886 Jul 25 04:44 VirusShare_00160.md5

for i in range(144, 161):
    counter = 0
    count = 0

    filenr = ("%0.5d" % i)
    command = 'wget http://virusshare.com/hashes/VirusShare_' + filenr + '.md5'
    os.system(command)
    filenaam = 'VirusShare_' + filenr + '.md5'
    db_comment = 'BAD HASH - Obtained from VirusShare.com. File: ' + filenaam
    with open(filenaam) as f:
        for line in f:
            counter += 1

    with open(filenaam) as f:
        startreadfiletime = time.time()
        print 'Reading file: VirusShare_' + filenr + '.md5'
        print 'Total lines in file: ' + str(counter)
        for line in f:
            count += 1
            if count % 1000 == 0:
                print 'Done reading ' + str(count) + ' lines'
            if not line.startswith('#'):
                line = line.strip('\n')
                sql_prefix = "bad_hashes where md5hash = '{}'".format(line)
                get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
                if not get_hash_from_db_tuple:
                    db_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql_line = "INSERT INTO bad_hashes VALUES (0, "
                    sql_line = sql_line + "'{}', '{}', '{}', '0')".format(line, db_time, db_comment)
                    try:
                        Lobotomy.exec_sql_query(sql_line, 'lobotomy')
                        hashcount += 1
                        print 'File: VirusShare_' + filenr + '.md5 - Hash:', line, 'added. Hashes added so far:', str(hashcount)
                    except:
                        print 'error'

        stopreadfiletime = time.time()
        print str(hashcount) + ' hashes addes to database so far.'
        print 'seconds to read file', round(stopreadfiletime - startreadfiletime)

stoptime = time.time()
print 'seconds to complete', round(stoptime - starttime)

