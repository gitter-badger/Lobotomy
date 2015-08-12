__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# 03-02: WV - Aanpassen SQL query tbv modificatie website en database
#
# 12 aug 2015:  WV
# Fixed parse error in date/time, column date.
# Fixed issue with some filesizes. changed database value from int to varchar.
#


import sys
import os
import main
import MySQLdb
from dateutil.parser import parse

Lobotomy = main.Lobotomy()

DEBUG = False


def memtimeliner(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = list()
    command.append('vol.py -f "' + imagename + '" --profile=' + imagetype + ' timeliner --output=body --output-file="'
                                                                            '' + imagename + '-timeliner_time"')
    command.append('vol.py -f "' + imagename + '" --profile=' + imagetype + ' shellbags --output=body --output-file="'
                                                                            '' + imagename + '-shellbagstime"')
    command.append('vol.py -f "' + imagename + '" --profile=' + imagetype + ' mftparser --output=body --output-file="'
                                                                            '' + imagename + '-mfttime"')
    command.append('cat "' + imagename + '-timeliner_time" "' + imagename + '-mfttime" "' + imagename +
                   '-shellbagstime" >> "' + imagename + '-bodytimeline.txt"')
    command.append('mactime -b "' + imagename + '-bodytimeline.txt" -d > "' + imagename + '-mactime.csv"')

    if DEBUG:
        for item in command:
            print item
    else:
        for item in command:
            Lobotomy.write_to_main_log(database, " Start: " + item)
            Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start: " + item)
            os.system(item)
            Lobotomy.write_to_main_log(database, " Stop : " + item)
            Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop : " + item)
        Lobotomy.write_to_main_log(database, " Start: Update database ")
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Start: Update database ")
        input_sql(imagename, database)
        Lobotomy.write_to_main_log(database, " Stop  : Update database")
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop : Update database")


def input_sql(imagename, database):
        with open(imagename + "-mactime.csv") as f:
            for line in f:
                if not line.startswith('Date,Size'):
                    listitem = line.split(',')
                    date = listitem[0]
                    try:
                        listitem[0] = parse(date).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        print 'Error parsing date/time, keeping original value:', listitem[0]
                    for i in range(len(listitem)):
                        listitem[i] = listitem[i].replace('\\', '\\\\')
                        listitem[i] = MySQLdb.escape_string(listitem[i])
                    if DEBUG:
                        print "VALUES {}, {}, {}, {}, {}, {}, {}, {}".format(listitem[0], listitem[1], listitem[2],
                                    listitem[3], listitem[4], listitem[5], listitem[6], listitem[7])
                    else:
                        Lobotomy.exec_sql_query("INSERT INTO memtimeliner (id, date, size, type, mode, uid, gid, "
                                    "meta, filename)VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format
                                    (listitem[0], listitem[1], listitem[2], listitem[3], listitem[4],
                                    listitem[5], listitem[6], listitem[7]), database)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: memtimeliner.py [database]"
    else:
        memtimeliner(sys.argv[1])
