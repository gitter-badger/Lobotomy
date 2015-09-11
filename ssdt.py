__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script version    0.6
# Plugin version:   1
# 08 mrt 2015:      Wim Venhuizen
# Plugin:           SSDT, Verbose
#
# Date:             11-09-2015
# Detail:           Revision of SSDT.
#                   New version includes the Verbose option

import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "ssdt"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + ' --verbose'

    if DEBUG:
        print "Write log: " + database + ", Start: " + command
        print "Write log: " + casedir + ", Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)

    if DEBUG:
        print command
    else:
        print "Running Volatility -", plugin, ", please wait."
        vollog = ""
        status, vollog = commands.getstatusoutput(command)

    if DEBUG:
        print "Write log: " + database + " Stop: " + command
        print "Write log: " + casedir + " Stop: " + command
    else:
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing volatility output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing volatility output: " + plugin)

    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(vollog)
        f.close()
    except:
        pass

    items = vollog.split('\n')
    print 'Parsing ' + plugin + ' data...'

    count = 0
    counter = 0
    for line in items:
        counter += 1

# [x86] Gathering all referenced SSDTs from KTHREADs...
# Finding appropriate address space for tables...
# SSDT[0] at 80501b8c with 284 entries
#   Entry 0x0000: 0x80599948 (NtAcceptConnectPort) owned by ntoskrnl.exe
#   Entry 0x004f: 0xb240f446 (NtFlushKey) owned by PROCMON20.SYS
#   Entry 0x0050: 0x805a1ab8 (NtFlushVirtualMemory) owned by ntoskrnl.exe
#   Entry 0x0051: 0x805abdda (NtFlushWriteBuffer) owned by ntoskrnl.exe
#   ** INLINE HOOK? => 0x806d76c2 (hal.dll)
#   Entry 0x0052: 0x805ab94a (NtFreeUserPhysicalPages) owned by ntoskrnl.exe
#   Entry 0x0054: 0x8056e476 (NtFsControlFile) owned by ntoskrnl.exe
#   Entry 0x011b: 0x805c1798 (NtQueryPortInformationProcess) owned by ntoskrnl.exe
# SSDT[1] at bf999b80 with 667 entries
#   Entry 0x1000: 0xbf935f7e (NtGdiAbortDoc) owned by win32k.sys

    ssdt = ''
    ssdtmem = ''
    entry = ''
    pointer = ''
    syscall = ''
    owner = ''
    hookaddress = ''
    hookprocess = ''

    for line in items:
        count += 1
        pct = str(float(1.0 * count / counter) * 100).split(".")[0]
        if line.startswith('SSDT'):
            ssdt = line.split(' ')[0]
            ssdtmem = line.split(' ')[2]
        if line.startswith('  Entry'):
            test = line.split(' ')
            entry = test[3].strip(':')
            pointer = test[4]
            syscall = test[5].strip('()')
            owner = test[8]
        if line.startswith('  ** INLINE'):
            hookaddress = line.split(' ')[6]
            hookprocess = line.split(' ')[7].strip('()')
            print 'Alert: Hookadress found!', ssdt, ssdtmem, entry, pointer, syscall, owner, hookaddress, hookprocess
        if entry != '' and line.split(' ')[2] == 'Entry':
            SQL_cmd = "INSERT INTO ssdt VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(ssdt, ssdtmem, entry,
                                                    pointer, syscall, owner, hookaddress, hookprocess)
            try:
                Lobotomy.exec_sql_query(SQL_cmd, database)
            except:
                print 'SQL Error in ', database, 'plugin: ', plugin
                print 'SQL Error: ',  SQL_cmd
                Lobotomy.write_to_case_log(casedir, "Database: " + database + " Error:  running plugin: " + plugin)
                Lobotomy.write_to_case_log(casedir, "Database: " + database + 'SQL line: ' + SQL_cmd)

            entry = ''
            pointer = ''
            syscall = ''
            owner = ''
            hookaddress = ''
            hookprocess = ''

        try:
            if pct != pcttmp:
                print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)
                Lobotomy.plugin_pct(plugin, database, pct)
        except:
            pass
        pcttmp = pct

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Stop:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, "Database: " + database + " Stop:  running plugin: " + plugin)
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
