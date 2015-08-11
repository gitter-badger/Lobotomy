__author__ = 'Wim Venhuizen'

#
# Script.version    0.2
# Date:             10-08-2015
# Edited:           W Venhuizen
# Import hashes from NIST.
# Downloadlink: http://www.nsrl.nist.gov/morealgs/md5b4096.zip
# Manual unzip and keep filename. run script from the same folder where the file is.

import time
from datetime import datetime
import main
Lobotomy = main.Lobotomy()

starttime = time.time()
hashcount = 0
counter = 0
count = 0

filenaam = 'md5b4096.txt'
db_comment = 'Known HASH - Obtained from Nist.gov. '

with open(filenaam) as f:
    for line in f:
        counter += 1

with open(filenaam) as f:
    startreadfiletime = time.time()
    print 'Reading file: ' + filenaam
    print 'Total lines in file: ' + str(counter)
    print 'Total hashes in file: ' + str(counter * 2) # every line have 2 hashes.
    for line in f:
        count += 1
        if count % 1000 == 0:
            print 'Done reading ' + str(count) + ' lines'
        if not line.startswith('#'):
            test = line.strip('\n').split('\t')
            for line in test:
                sql_prefix = "bad_hashes where md5hash = '{}'".format(line)
                get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
                if not get_hash_from_db_tuple:
                    db_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql_line = "INSERT INTO bad_hashes VALUES (0, "
                    sql_line = sql_line + "'{}', '{}', '{}', '0')".format(line, db_time, db_comment)
                    try:
                        Lobotomy.exec_sql_query(sql_line, 'lobotomy')
                        hashcount += 1
                        print 'File: ' + filenaam + ' - Hash:', line, 'added. Hashes added so far:', str(hashcount)
                    except:
                        print 'error'

    stopreadfiletime = time.time()
    print str(hashcount) + ' hashes addes to database so far.'
    print 'seconds to read file', round(stopreadfiletime - startreadfiletime)
