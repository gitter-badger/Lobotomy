__author__ = 'Wim Venhuizen'

#
# Script.version    0.3
# Date:             08-03-2015
# Edited:           W Venhuizen
#
# Eerste opzet om bad_hashes op te halen van virusshare
#
# Date:             08-08-2015
# Edited:           W Venhuizen
# Wegschrijven logfile, lezen logfile en parsen website virusshare.
#
# Date:             11 aug 2015
# Edited:           W Venhuizen
# Eerste opzet voor offline mode. moet nog getest worden. (beta)
#


import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()
plugin = 'get_hashes_from_virusshare'

starttime = time.time()
hashcount = 0
test = 0
get_from = 0
get_to = 1


def main(optie, folder):
    if optie == '-o':
        print 'Running in offline modes!'

    try:
        with open(plugin + '.txt', 'r') as f:
            for line in f:
                if line.startswith('VirusShare_'):
                    test = line.split('_')[1].split('.')[0]
        get_from = int(test)
        print 'Last updated at: ' + line.split('.')[1].split('\t')[2].strip('\n')
    except:
        pass

    if optie == '-i':
        print "Parsing website virusshare, please wait."
        command = 'curl http://virusshare.com/hashes.4n6'
        log = ""
        status, log = commands.getstatusoutput(command)
        log = log.split('\n')

        for line in log:
            if line.startswith('<a href="hashes/VirusShare_'):
                test = line.split('_')[1].split('.')[0]
            get_to = int(test)
    else:
        # read local files
        count = 0
        for subdir, dirs, files in os.walk(os.path.dirname(folder)):
            for file in files:
                filenaam = os.path.join(subdir, file)
                if filenaam.endswith('.md5'):
                    print filenaam
                    count = count +1
        get_to = count - 1

    if get_from == get_to:
        print 'No need to update, exit'
        exit()

    for i in range(get_from + 1, get_to + 1):
        counter = 0
        count = 0

        filenr = ("%0.5d" % i)
        if optie == '-i':
            command = 'wget http://virusshare.com/hashes/VirusShare_' + filenr + '.md5'
            os.system(command)
        else:
            pass# offline modes

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

        try:
            f = open(plugin + '.txt', 'a')
            f.write(filenaam + '\t\t' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.close()
            print 'updating logfile'
        except:
            f = open(plugin + '.txt', 'w')
            f.write(filenaam + '\t\t' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.close()
            print 'Creating and updating logfile'

    stoptime = time.time()
    print 'seconds to complete', round(stoptime - starttime)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: " + plugin + ".py -o (offline modes) <folder>"
        print "Usage: " + plugin + ".py -i (internet modes)"
    else:
        folder = ''
        try:
            folder = sys.argv[2]
        except:
            pass
        main(sys.argv[1], folder)

