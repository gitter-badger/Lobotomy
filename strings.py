__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# Script version    0.6
# Plugin version:   1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           Strings
# Edit:             15 sep 2015
# Detail:           Change: Save strings output in casefolder, not database.
#                   Change: Not using os.system, but commands.

import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "strings"

DEBUG = False

def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]

    command = "strings -tx {}".format(imagename)
    
    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        print "Running ", plugin, ", please wait."
        vollog = ""
        status, log = commands.getstatusoutput(command)

        
    if DEBUG:
        print "Write log: " + database + ", Stop: " + command
        print "Write log: " + casedir + ", Stop: " + command
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: running plugin: " + plugin)

    # *\ done
    # Strings needs to be exported to a file, not database.

    print 'Writing ' + plugin + ' data...'

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(log)
        f.close()
    except:
        pass

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop: running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Stop: running plugin: " + plugin)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
