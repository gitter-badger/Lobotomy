__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# Script version    0.5
# Plugin version    0.7.1
# Date:             06-07-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Eerste opzet yarascan voor lobotomy.
#
# Date:             14-07-2015
# Aanpassing yarascan zodat het ook met autostart kan werken. foldernaam is optioneel.
# Als de folernaam niet is opgegeven worden alle files in alle subfolder(s) van de imagefolder gescaned.
#
# Date:             30 aug  2015
# change line 61: print "Running yarascan on folder: " + filename : change to : subdir1
# change line 77: Removing space char in output.



import sys
import main
import commands
import os

Lobotomy = main.Lobotomy()
plugin = "yarascan"

DEBUG = False


def main(database, folder):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    sql_prefix = "INSERT INTO yarascan VALUES (0, "
    counter = 0
    count = 0
    sql_line = ''

    if folder == '':

        for subdir, dirs, files in os.walk(casedir):
            for folders in dirs:
                for subdir1, dirs1, files1 in os.walk(subdir + '/' + folders):
                    for file in files1:
                        counter += 1

        for subdir, dirs, files in os.walk(casedir):
            for folders in dirs:
                for subdir1, dirs1, files1 in os.walk(subdir + '/' + folders):
                    for file in files1:
                        count = count +1
                        filenaam = os.path.join(subdir1, file)
                        command = "yara yara_rules/index.yara " + filenaam + " -m -s"
                        if DEBUG:
                            print command
                        else:
                            print "Running yarascan on folder: " + subdir1
                            log = ""
                            status, log = commands.getstatusoutput(command)
                        if DEBUG:
                            print "Write log: " + database + ", Start: " + command
                            print "Write log: " + casedir + ", Start: " + command
                        else:
                            Lobotomy.write_to_main_log(database, " Start: " + command)
                            Lobotomy.write_to_case_log(casedir, " Start: " + command)
                        try:
                            pct = str(float(1.0 * count / counter) * 99).split(".")[0]
                            print "Yarascan - Percentage done: ", pct
                        except:
                            pass
                        print "Yarascan - Files to go: " + str(counter) + " from " + str(count)
                        print "Yarascan - Current filename:", filenaam
                        if log != '':
                            for item in log.split('\n'):
                                if filenaam in item:
                                    #count += 1

                                    yara = item.split('[')[0]
                                    if 'description' in item:
                                        start = int(item.find('description')+13)
                                        yara_description = item[start:].split('"')[0]
                                        filename = "/" + item.split('/', 1)[1].replace('//', '/')
                                else:
                                    a = item.split(':')
                                    try:
                                        offset = a[0]
                                    except:
                                        offset = ''
                                    try:
                                        description = a[1]
                                    except:
                                        description = ''
                                    try:
                                        string = a[2]
                                    except:
                                        string = ''
                                    try:
                                        sql_line = sql_prefix + "'{}', '{}', '{}', '{}', '{}', '{}'".format(filename,\
                                                offset, description, string, yara, yara_description + "')")[:-1]
                                        Lobotomy.exec_sql_query(sql_line, database)
                                        Lobotomy.plugin_pct(plugin, database, pct)
                                    except:
                                        print 'Error sql query: ' + sql_line + " - " + database

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing Yara output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing Yara output: " + plugin)

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: " + plugin + ".py <database> <folder>"
    else:
        folder = ''
        try:
            folder = sys.argv[2]
        except:
            pass
        main(sys.argv[1], folder)

