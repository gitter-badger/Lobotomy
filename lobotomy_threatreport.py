# coding=utf-8
__author__ = 'Wim Venhuizen'

#
# Script version    0.2
# Plugin version:   0.1
# 08 mrt 2015:      Wim Venhuizen
# Plugin:           Lobotomy threat scanner and report
#
# 07 okt 2015:      Wim Venhuizen
# Detail:           Added Impscan to report.


import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()
plugin = "threatreport"
DEBUG = False


report = ''
report_index = []
report_body = []
report_appendix = []
report_explain = []
lobotomy_report = ''
lobotomy_scan_Hashes = ''
lobotomy_scan_Process = ''
lobotomy_scan_Modules = ''
lobotomy_scan_SSDT_hooks = ''
lobotomy_scan_API_hooks = ''
lobotomy_scan_IDT_hooks = ''
lobotomy_scan_Mutex = ''
lobotomy_scan_Yara = ''
lobotomy_scan_Malfind = ''
bad_hashes_list = []

# todo

# Done - OrphanThread = 'Detect orphan threads',
#        Orphan threads scanner - read threads without pid from psxview.
# SystemThread = 'Detect system threads',
# Done: HookedSSDT = 'Detect threads using a hooked SSDT'
# ScannerOnly = 'Detect threads no longer in a linked list',
# DkomExit = 'Detect inconsistencies wrt exit times and termination',
# HideFromDebug = 'Detect threads hidden from debuggers',
# HwBreakpoints = 'Detect threads with hardware breakpoints',
# AttachedProcess = 'Detect threads attached to another process',


# ldrmodules: exe -> path naar exe -> controleer imports (base address) als true,false,true
# Pid	Process	    Base	    Inload	Ininit	Inmem	Mappedpath
# 680 	lsass.exe 	0x01000000 	True 	False 	True 	\WINDOWS\system32\lsass.exe
# 868 	lsass.exe 	0x01000000 	True 	False 	True
# bij exe (is een verwijzing naar zichzelf) ininit is altijd false
# lege mappedpath kan malicious zijn.
# get imports met impscan, baseaddress and pid

# ldrmodules: exe -> path exe leeg -> controleer imports (base address) als false,false,false
# 1928 	lsass.exe 	0x00080000 	False 	False 	False
# Controleren: inload en inmem op false, kan geen imports hebben, anders malicious, scan voor pe of mz header, carve exe/dll
# get imports met impscan, baseaddress and pid

# ldrmodules: exe -> dll -> controleer imports (base address) als true,false,true
# Pid	Process	    Base	    Inload	Ininit	Inmem	Mappedpath
# 1928 	lsass.exe 	0x01000000 	True 	False 	True
#


def main(database):
    global lobotomy_report
    global lobotomy_threatlist
    global imagetype
    global data_dlldump
    global data_moddump
    global data_procdump
    global data_photorec
    global data_vol_yara
    global data_yara
    global data_exifinfo
    global data_pe_scan
    global data_pe_scan_beta
    global data_psxview
    global data_pstree
    global data_malfind
    global data_driverscan
    global call_timer

    a = 'ABCDEFGHIJKLMNOP'
    Lobotomy.plugin_start('lobotomy_report', database)
    Lobotomy.plugin_pct('lobotomy_report', database, 1)

    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]

    lobotomy_threatlist = read_threatlist_from_file()

    # Read database
    call_timer = []

    data_dlldump = Lobotomy.get_databasedata('fullfilename,modulename,filename,md5', 'dlldump', database)
    data_moddump = Lobotomy.get_databasedata('fullfilename,modulename,filename,md5,modulebase', 'moddump', database)
    data_procdump = Lobotomy.get_databasedata('fullfilename,name,filename,md5', 'procdump', database)
    data_photorec = Lobotomy.get_databasedata('fullfilename,filemd5', 'photorec', database)
    data_vol_yara = Lobotomy.get_databasedata('owner_name,pid,rule,data_offset,data_bytes,data_txt',
                                              'volatility_yarascan', database)
    data_yara = Lobotomy.get_databasedata('filename,string,yara,yara_description', 'yarascan', database)
    data_exifinfo = Lobotomy.get_databasedata('Filename,Exifinfo', 'exifinfo', database)
    data_pe_scan = Lobotomy.get_databasedata('Fullfilename,Pe_Compiletime,Pe_Packer,Filetype,Original_Filename,Yara_Results'
                                             , 'pe_scan', database)
    data_pe_scan_beta = Lobotomy.get_databasedata('Filename,Pe_Blob', 'pe_scanner_beta', database)
    data_psxview = Lobotomy.get_databasedata('offset,name,pid,pslist,psscan,thrdproc,pspcid,csrss,session,deskthrd,'
                                             'exittime', 'psxview', database)
    data_pstree  = Lobotomy.get_databasedata('depth,offset,name,pid,ppid,thds,hnds,plugin_time,audit,cmd,path',
                                             'pstree', database)
    data_malfind = Lobotomy.get_databasedata('process,pid,address,vadtag,protection,flags,header,body',
                                             'malfind', database)

    bad_hashes_list = []
    # Compare the hash from ddldump, procdump and photorec with the hashes in the database, bad_hashes
    # if there is no match, there will be no trigger for the program to collect data.

    # Build a list of the scanned items.

    # Scan for hashes

    report = ''
    report, bad_hashes_list = lobotomy_scan_bad_hashes(data_dlldump, data_moddump, data_procdump, data_photorec)
    if report != '':
        report_index.append('Scanned Bad Hashes')
        report_body.append(['Scanned Bad Hashes', report])
        report = ''
        report = filescan_bad_hashes(bad_hashes_list)
        report_index.append('Appendix: Bad Hashes')
        report_appendix.append(['Appendix: Bad Hashes', report])

    # Scan for Unlinked DLL's
    report, report_fileinfo = unlinked_dlls(database)
    if report != '':
        report_index.append('Scanned Unlinked dlls')
        report_body.append(['Scanned Unlinked dlls', report])
        report_index.append('Appendix: Unlinked dlls')
        report_appendix.append(['Appendix: Unlinked dlls', report_fileinfo])

    report, report_fileinfo = suspicious_modules(database)
    if report != '':
        report_index.append('Scanned Suspicious Modules')
        report_body.append(['Scanned Suspicious Modules', report])
        report_index.append('Appendix: Suspicious Modules')
        report_appendix.append(['Appendix: Suspicious Modules', report_fileinfo])

    # Scan for SSDT hooking
    report = ssdt_hooking(database)
    if report != '':
        explain = lobotomy_explain('SSDT Hooking')
        report_index.append('Scanned SSDT Inline Hooking')
        report_body.append(['Scanned SSDT Inline Hooking', report])
        report_index.append('Explanation SSDT Inline Hooking')
        report_explain.append(['Explanation SSDT Inline Hooking', explain])
        # report_index.append('Appendix: SSDT Hooking')
        # report_appendix.append(['Appendix: SSDT Hooking', report_fileinfo])

    report = Malicious_Callbacks(database)
    if report != '':
        report_index.append('Scanned Malicious Callbacks')
        report_body.append(['Scanned Malicious Callbacks', report])
        # report_index.append('Appendix: Malicious Callbacks')
        # report_appendix.append(['Appendix: Malicious Callbacks', report_fileinfo])

    report = Malicious_Callbacks_Custom(database)
    if report != '':
        report_index.append('Scanned Custom Malicious Callbacks')
        report_body.append(['Scanned Custom Malicious Callbacks', report])
        # report_index.append('Appendix: Custom Malicious Callbacks')
        # report_appendix.append(['Appendix: Custom Malicious Callbacks', report_fileinfo])

    report = Malicious_Timers(database)
    if report != '':
        explain = lobotomy_explain('Malicious_Timers')
        report_index.append('Scanned Custom Malicious Timers')
        report_body.append(['Scanned Custom Malicious Timers', report])
        report_explain.append(['Scanned Custom Malicious Timers', explain])
        # report_index.append('Appendix: Custom Malicious Callbacks')
        # report_appendix.append(['Appendix: Custom Malicious Callbacks', report_fileinfo])

    report = lobotomy_orphan_threadscan(database)
    if report != '':
        explain = lobotomy_explain('Orphan thread')
        report_index.append('Scanned Orphan thread')
        report_body.append(['Scanned Orphan thread', report])
        report_explain.append(['Scanned Orphan thread', explain])
        # report_index.append('Appendix: Custom Malicious Callbacks')
        # report_appendix.append(['Appendix: Custom Malicious Callbacks', report_fileinfo])

    report, report_fileinfo = lobotomy_msfdetect(database)
    if report != '':
        #explain = lobotomy_explain('MSF')
        report_index.append('Scanned MSF')
        report_body.append(['Scanned MSF', report])
        #report_explain.append(['Scanned MSF', explain])
        report_index.append('Appendix: Scanned MSF')
        report_appendix.append(['Appendix: Scanned MSF', report_fileinfo])

    lobotomy_report = 'Lobotomy Memory Report\n'
    lobotomy_report += '#' * 64 + '\n'
    count_reports = 0
    count_appendix = 0
    for item_index in report_index:
        if not item_index.startswith('Appendix') and not item_index.startswith('Explanation'):
            count_reports += 1
            lobotomy_report += '\n{}.\t{}'.format(count_reports, item_index)
    for item_index in report_index:
        if item_index.startswith('Appendix'):
            lobotomy_report += '\n{}.\t{}'.format(a[count_appendix], item_index)
            count_appendix += 1
    for item_index in report_index:
        if item_index.startswith('Explanation'):
            lobotomy_report += '\n{}.\n'.format(item_index)
            count_appendix += 1

    lobotomy_report += '\n' * 3
    lobotomy_report += 'Keep in mind:\n'
    lobotomy_report += "If lobotomy didn't find anything, doesn't mean there isn't anything to find.\n"
    lobotomy_report += "Maybe we don't have the plugin yet or haven't build it yet.\n"
    lobotomy_report += '\n' * 3

    count_index = 0
    for item_index in report_index:
        if not item_index.startswith('Appendix') and not item_index.startswith('Explanation'):
            count_index += 1
            for item_body in report_body:
                if item_body[0] == item_index:
                    lobotomy_report += '{}.\t{}\n'.format(count_index, item_body[0])
                    lobotomy_report += '#' * 120
                    lobotomy_report += '\n\n{}\n\n'.format(item_body[1])

    count_appendix = 0
    for item_index in report_index:
        if item_index.startswith('Appendix'):
            for item_appendix in report_appendix:
                if item_appendix[0] == item_index:
                    lobotomy_report += '{}.\t{}\n'.format(a[count_appendix], item_appendix[0])
                    lobotomy_report += '#' * 120
                    lobotomy_report += '\n\n{}\n\n'.format(item_appendix[1])
                    count_appendix += 1

    count_explain = 0
    for item_index in report_index:
        if item_index.startswith('Explanation'):
            for item_explain in report_explain:
                if item_explain[0] == item_index:
                    lobotomy_report += '{}.\n'.format(item_explain[0])
                    lobotomy_report += '#' * 120
                    lobotomy_report += '{}'.format(item_explain[1])
                    count_appendix += 1


    lobotomy_report += '\n\nReport is generated by Lobotomy.'
    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(lobotomy_report)
        f.close()
    except:
        pass

    if DEBUG:
        print SQL_cmd
    else:
        lobotomy_report = lobotomy_report.replace('\\', '\\\\')
        lobotomy_report = lobotomy_report.replace("'", '"')
        SQL_cmd = "INSERT INTO lobotomy_report VALUES (0, '{}')".format(lobotomy_report)
        Lobotomy.exec_sql_query(SQL_cmd, database)
        Lobotomy.plugin_stop('lobotomy_report', database)
        Lobotomy.plugin_pct('lobotomy_report', database, 100)

    print lobotomy_report
    exit()


def Malicious_Callbacks(database):
#########################################################################################
#########################################################################################
# Malicious Callbacks
# Many high-profile rootkits such as Mebroot, ZeroAccess, Rustock, Ascesso, Tigger, Stuxnet,
# Blackenergy, and TDL3 leverage kernel callbacks. In most cases, they also try to hide by
# unlinking the KLDR_DATA_TABLE_ENTRY or by running as an orphan thread from a kernel
# pool. This behavior makes the malicious callbacks easy to spot because the Module column
# in the output of Volatility’s callbacks plugin displays UNKNOWN . In other cases, malware
# authors don’t hide their module at all, but they use a hard-coded (and thus predictable)
# name with which you can build indicators of compromise (IOCs).
# The first example is from Stuxnet. It loads two modules: mrxnet.sys and mrxcls.sys .
# The first one installs a file system registration change callback to receive notification when
# new file systems become available (so it can immediately spread or hide files). The second
# one installs an image load callback, which it uses to inject code into processes when they
# try to load other dynamic link libraries (DLLs).
#########################################################################################
#########################################################################################
    report = ''
    report_fileinfo = ''
    call_timer = []
    callbacktype_from_file = []
    callbackmodule_from_file = []

    data_callbacks = Lobotomy.get_databasedata('type,callback,module,details', 'callbacks', database)

    for line in lobotomy_threatlist:
        if not line.startswith('#'):
            if line.startswith('callbacks:type'):
                callbacktype_from_file.append(line.strip('\n').split(':')[2])
            if line.startswith('callbacks:module'):
                callbackmodule_from_file.append(line.strip('\n').split(':')[2])

    alertcallbackmodule = 0
    for line_callbacks in data_callbacks:
        type_callbacks, callback_callbacks, module_callbacks, details_callbacks = line_callbacks
        if module_callbacks == 'UNKNOWN':
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if alertcallbackmodule == 0:
                report += 'Searching for: Malicious Callbacks'
                report += 'Alert: Unknown Module in Callback: \n'
                report += '\n' + '*' * 120 + '\n'
                alertcallbackmodule = 1
            report += '\nType     : ' + str(line_callbacks[0])
            report += '\nCallback : ' + str(line_callbacks[1])
            report += '\nModule   : ' + str(line_callbacks[2])
            report += '\nDetails  : ' + str(line_callbacks[3]) + '\n'
            tmp = module_callbacks, line_callbacks
            call_timer.append(tmp)
            # module_callbacks = ''

    return report
    
    
def Malicious_Callbacks_Custom(database):
    report = ''
    report_fileinfo = ''
    callbacktype_from_file = []
    callbackmodule_from_file = []
    alertcallbackmodulefile = 0
    alertcallbacktypefile = 0

    data_callbacks = Lobotomy.get_databasedata('type,callback,module,details', 'callbacks', database)

    for line in lobotomy_threatlist:
        if not line.startswith('#'):
            if line.startswith('callbacks:type'):
                callbacktype_from_file.append(line.strip('\n').split(':')[2])
            if line.startswith('callbacks:module'):
                callbackmodule_from_file.append(line.strip('\n').split(':')[2])

    for line_callbacks in data_callbacks:
        type_callbacks, callback_callbacks, module_callbacks, details_callbacks = line_callbacks

        for callback_alert in callbacktype_from_file:
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if type_callbacks == callback_alert:
                if alertcallbacktypefile == 0:
                    report += '\n' + '*' * 120 + '\n\n'
                    report += "Alert: Callback 'Type' from Lobotomy Threatlist: \n"
                    alertcallbacktypefile = 1
                report += '\nType     : ' + str(line_callbacks[0])
                report += '\nCallback : ' + str(line_callbacks[1])
                report += '\nModule   : ' + str(line_callbacks[2])
                report += '\nDetails  : ' + str(line_callbacks[3]) + '\n'
                tmp = module_callbacks, line_callbacks
                call_timer.append(tmp)

        for callback_alert in callbackmodule_from_file:
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if module_callbacks == callback_alert:
                if alertcallbackmodulefile == 0:
                    report += '\n' + '*' * 120 + '\n'
                    report += "Alert: Callback 'Module' from Lobotomy Threatlist: \n"
                    alertcallbackmodulefile = 1
                report += '\nType     : ' + str(line_callbacks[0])
                report += '\nCallback : ' + str(line_callbacks[1])
                report += '\nModule   : ' + str(line_callbacks[2])
                report += '\nDetails  : ' + str(line_callbacks[3]) + '\n'
                tmp = module_callbacks, line_callbacks
                # call_times is needed for module timers
                call_timer.append(tmp)

    return report


def Malicious_Timers(database):    
    data_callbacks = Lobotomy.get_databasedata('type,callback,module,details', 'callbacks', database)
    data_timers = Lobotomy.get_databasedata('offset,duetime,period,signaled,routine,module', 'timers', database)
    data_driverscan = Lobotomy.get_databasedata('offset,ptr,hnd,start,size,servicekey,name,drivername', 'driverscan', database)

    report = ''
    report_fileinfo = ''

    alerttimercallback = 0
    for line_timers in data_timers:
        offset_timers, duetime_timers, period_timers, signaled_timers, routine_timers, module_timers = line_timers
        if module_timers == 'UNKNOWN':
            if alerttimercallback == 0:
                report += 'Searching for: Malicious Timers'
                report += '\nAlert: Unknown Module in Timers:'
                alerttimercallback = 1
            report += '\nOffset   : ' + str(line_timers[0])
            report += '\nDuetime  : ' + str(line_timers[1])
            report += '\nPeriod   : ' + str(line_timers[2])
            report += '\nSignaled : ' + str(line_timers[3])
            report += '\nRoutine  : ' + str(line_timers[4])
            report += '\nModule   : ' + str(line_timers[5]) + '\n'
            for line_callbacks in data_callbacks:

                for line_driverscan in data_driverscan:
                    offset_driverscan, ptr_driverscan, hnd_driverscan, start_driverscan, size_driverscan, \
                        servicekey_driverscan, name_driverscan, drivername_driverscan = line_driverscan

                    if str(line_callbacks[2]) == str(line_driverscan[6]):   # callbacks.details matches driverscan.drivername
                        report += '\nWe might have a match between the name from Plugin Callbacks and ' \
                                  'Driverscan:\nDrivername:' + str(drivername_driverscan)
                        report += '\nPlugin Driverscan : ' + str(line_driverscan[6])
                        report += '\nOffset            : ' + str(line_driverscan[0])
                        report += '\nPtr               : ' + str(line_driverscan[1])
                        report += '\nHnd               : ' + str(line_driverscan[2])
                        report += '\nStart             : ' + str(line_driverscan[3])
                        report += '\nSize              : ' + str(line_driverscan[4])
                        report += '\nServicekey        : ' + str(line_driverscan[5])
                        report += '\nName              : ' + str(line_driverscan[6])
                        report += '\nDrivername        : ' + str(line_driverscan[7])
                        report += '\n\nPlugin Callbacks : ' + str(line_callbacks[2])
                        report += '\nType     : ' + str(line_callbacks[0])
                        report += '\nCallback : ' + str(line_callbacks[1])
                        report += '\nModule   : ' + str(line_callbacks[2])
                        report += '\nDetails  : ' + str(line_callbacks[3]) + '\n'

    return report


def read_threatlist_from_file():
    lobotomy_threatlist = []
    # Read Local lobotomy_threatlist.txt (case folder) for extra IOC's or custom searches.
    try:
        with open(casedir + '/lobotomy_threatlist.txt') as f:
            for line in f:
                if not line.startswith('#'):
                    lobotomy_threatlist.append(line)
    except:
        pass # No lobotomy_threatlist.txt found in case folder. Continue.

    # Read Global lobotomy_threatlist.txt for extra IOC's or custom searches.
    with open('lobotomy_threatlist.txt') as f:
        for line in f:
            if not line.startswith('#'):
                lobotomy_threatlist.append(line)
    return lobotomy_threatlist


def lobotomy_scan_bad_hashes(data_dlldump, data_moddump, data_procdump, data_photorec):
    global lobotomy_scan_Hashes
    #global bad_hashes_list
    for line_dlldump in data_dlldump:
        fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = line_dlldump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_dlldump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_dlldump:
                    lobotomy_scan_Hashes += '\n***********************************' + '\n'
                    lobotomy_scan_Hashes += 'Plugin   : Dlldump ' + '\n'
                    lobotomy_scan_Hashes += 'Hash     : ' + md5hash_dlldump + '\n'
                    lobotomy_scan_Hashes += 'Filename : ' + filename_dlldump + '\n'
                    lobotomy_scan_Hashes += 'Module   : ' + modulename_dlldump + '\n'
                    bad_hashes_list.append(['dlldump', fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump])

    for line_moddump in data_moddump:
        fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump, modulebase_moddump = line_moddump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_moddump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_moddump:
                    lobotomy_scan_Hashes += '\n***********************************' + '\n'
                    lobotomy_scan_Hashes += 'Plugin   : Moddump ' + '\n'
                    lobotomy_scan_Hashes += 'Hash     : ' + md5hash_moddump + '\n'
                    lobotomy_scan_Hashes += 'Filename : ' + filename_moddump + '\n'
                    lobotomy_scan_Hashes += 'Base     : ' + modulebase_moddump + '\n'
                    lobotomy_scan_Hashes += 'Module   : ' + modulename_moddump + '\n'
                    bad_hashes_list.append(['moddump', fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump, modulebase_moddump])

    for line_procdump in data_procdump:
        fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = line_procdump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_procdump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_procdump:
                    lobotomy_scan_Hashes += '\n***********************************' + '\n'
                    lobotomy_scan_Hashes += 'Plugin   : Procdump ' + '\n'
                    lobotomy_scan_Hashes += 'Hash     : ' + md5hash_procdump + '\n'
                    lobotomy_scan_Hashes += 'Filename : ' + filename_procdump + '\n'
                    lobotomy_scan_Hashes += 'Name     : ' + name_procdump + '\n'
                    bad_hashes_list.append(['procdump', fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump])

    for line_photorec in data_photorec:
        fullfilename_photorec, md5hash_photorec = line_photorec
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_photorec.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_photorec:
                    lobotomy_scan_Hashes += '\n***********************************' + '\n'
                    lobotomy_scan_Hashes += 'Plugin   : Photorec ' + '\n'
                    lobotomy_scan_Hashes += 'Hash     : ' + md5hash_photorec + '\n'
                    lobotomy_scan_Hashes += 'Filename : ' + fullfilename_photorec + '\n'
                    bad_hashes_list.append(['photorec', fullfilename_photorec, md5hash_photorec])

    return lobotomy_scan_Hashes, bad_hashes_list


def filescan_bad_hashes(bad_hashes_list):
    report_info = ''
    for item in bad_hashes_list:
        if item[0] == 'dlldump':
            a, fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = item
            pid_dlldump = filename_dlldump.split('.')[1]
            report_info += '\n***********************************\n'
            report_info += 'collecting info for file : ' + fullfilename_dlldump + '\n'
            report_info += 'Name from dlldump        : ' + modulename_dlldump + '\n'
            report_info += 'Filename from dlldump    : ' + filename_dlldump + '\n'
            report_info += 'MD5 Hash from dlldump    : ' + md5hash_dlldump + '\n'
            report_info += 'Pid from dlldump         : ' + pid_dlldump + '\n'
            report_info += '***********************************\n' + '\n'

            # Get extra data for dlldump
            report_info += lobotomy_build_pstree(pid_dlldump)
            report_info += lobotomy_volyarascan(pid_dlldump, fullfilename_dlldump)
            report_info += lobotomy_exifinfo(fullfilename_dlldump)
            report_info += lobotomy_pe_scan(fullfilename_dlldump)

        # Collect data where procdump is the source (md5).

        if item[0] == 'procdump':
            a, fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = item
            pid_procdump = filename_procdump.split('.')[1]
            report_info += '\n***********************************' + '\n'
            report_info += 'collecting info for file : ' + fullfilename_procdump + '\n'
            report_info += 'Name from procdump       : ' + name_procdump + '\n'
            report_info += 'Filename from procdump   : ' + filename_procdump + '\n'
            report_info += 'MD5 Hash from procdump   : ' + md5hash_procdump + '\n'
            report_info += 'Pid from procdump        : ' + pid_procdump + '\n'
            report_info += '***********************************\n' + '\n'

            # Get extra data for procdump
            report_info += lobotomy_psxview(pid_procdump)
            report_info += lobotomy_build_pstree(pid_procdump)
            report_info += lobotomy_volyarascan(pid_procdump, fullfilename_procdump)
            report_info += lobotomy_exifinfo(fullfilename_procdump)
            report_info += lobotomy_pe_scan(fullfilename_procdump)

        if item[0] == 'moddump':
            a, fullfilename_moddump, name_moddump, filename_moddump, md5hash_moddump, modulename_moddump = item
            pid_moddump = filename_moddump.split('.')[1]
            report_info += '\n***********************************' + '\n'
            report_info += 'collecting info for file : ' + fullfilename_moddump + '\n'
            report_info += 'Name from moddump        : ' + name_moddump + '\n'
            report_info += 'Filename from moddump    : ' + filename_moddump + '\n'
            report_info += 'Module from moddump      : ' + modulename_moddump + '\n'
            report_info += 'MD5 Hash from moddump    : ' + md5hash_moddump + '\n'
            #report_info += 'Pid from moddump         : ' + pid_moddump + '\n' # Moddump heeft geen PID
            report_info += '***********************************\n\n'

            # Get extra data for moddump
            report_info += lobotomy_psxview(pid_moddump)
            report_info += lobotomy_build_pstree(pid_moddump)
            report_info += lobotomy_volyarascan(pid_moddump, fullfilename_moddump)
            report_info += lobotomy_exifinfo(fullfilename_moddump)
            report_info += lobotomy_pe_scan(fullfilename_moddump)

        # Collect data where photorec is the source (md5).
        if item[0] == 'photorec':
            a, fullfilename_photorec, md5hash_photorec = item
            for line_yara in data_yara:
                filename_yara, string_yara, yara_yara, yara_description_yara = line_yara
                if filename_yara == fullfilename_photorec:
                    report_info += 'Match - Photorec vs volatility_Yara'
                    report_info += '\n' + '*' * 120 + '\n'
                    report_info += 'Fullfilename        : ' + fullfilename_photorec + '\n'
                    report_info += 'MD5 Hash            : ' + md5hash_photorec + '\n'
                    report_info += 'Filename Yara       : ' + filename_yara + '\n'
                    report_info += 'Yara string         : ' + string_yara + '\n'
                    report_info += 'yara                : ' + yara_yara + '\n'
                    report_info += 'Yara description    : ' + yara_description_yara + '\n\n'

            # get extra data for photorec
            report_info += lobotomy_exifinfo(fullfilename_photorec)
            report_info += lobotomy_pe_scan(fullfilename_photorec)

    return report_info


def unlinked_dlls(database):
#########################################################################################
#########################################################################################
#   Find unlinked dll's with ldrmodules. (inload, Ininit, Inmem = false)
#   - alert if ininit is false and mappedpath is empty!
#   SELECT * FROM `ldrmodules_v` WHERE mappedpath = '' AND ininit = 'False';
#########################################################################################
#########################################################################################

    report_fileinfo = ''
    report = ''
    data_ldrmod = Lobotomy.get_databasedata('pid,process,base,inload,ininit,inmem,mappedpath,loadpathpath,'
                                            'loadpathprocess, initpathpath, initpathprocess, mempathpath,'
                                            'mempathprocess', 'ldrmodules_v', database)

    for line_ldrmodules in data_ldrmod:
        ldr_pid, ldr_process, ldr_base, ldr_inload, ldr_ininit, ldr_inmem, ldr_mappedpath, ldr_loadpathpath, \
        ldr_loadpathprocess, ldr_initpathpath, ldr_initpathprocess, ldr_mempathpath, ldr_mempathprocess = line_ldrmodules

        if ldr_mappedpath == '' and ldr_ininit == 'False':
            report += 'Possible unlinked Dll found' + '\n'
            report += 'Empty Ldr_Mappedpath and Ldr_ininit is False: Alert'
            report += '\n' + '*' * 120 + '\n'
            report += 'Process         : ' + ldr_process + '\n'
            report += 'Mapped Path     : ' + ldr_mappedpath + '\n'
            report += 'Base            : ' + ldr_base + '\n'
            report += 'Pid Ldrmodules  : ' + str(ldr_pid) + '\n'
            report += 'Inload          : ' + ldr_inload + '\n'
            report += 'Inload process  : ' + ldr_loadpathprocess + '\n'
            report += 'Inload path     : ' + ldr_loadpathpath + '\n'
            report += 'Ininint         : ' + ldr_ininit + '\n'
            report += 'Ininint process : ' + ldr_initpathprocess + '\n'
            report += 'Ininint path    : ' + ldr_initpathpath + '\n'
            report += 'Inmem           : ' + ldr_inmem + '\n'
            report += 'Inmem process   : ' + ldr_mempathprocess + '\n'
            report += 'Inmem path      : ' + ldr_mempathpath + '\n\n'

            # get extra data for unlinked dll's
            report_fileinfo += lobotomy_psxview(ldr_pid)
            report_fileinfo += lobotomy_build_pstree(ldr_pid)
            report_fileinfo += lobotomy_impscan(str(ldr_pid), str(ldr_base), database)
            report_fileinfo += lobotomy_malfind_info(ldr_pid, ldr_base)

    return report, report_fileinfo


def suspicious_modules(database):
#########################################################################################
#########################################################################################
#   Find suspicious modules with ldrmodules. 
#   - Alert if inload, Ininit, Inmem = True and if mappedpath isn't matching
#########################################################################################
#########################################################################################

    report_fileinfo = ''
    report = ''
    data_ldrmod = Lobotomy.get_databasedata('pid,process,base,inload,ininit,inmem,mappedpath,loadpathpath,'
                                            'loadpathprocess, initpathpath, initpathprocess, mempathpath,'
                                            'mempathprocess', 'ldrmodules_v', database)

    for line_ldrmodules in data_ldrmod:
        ldr_pid, ldr_process, ldr_base, ldr_inload, ldr_ininit, ldr_inmem, ldr_mappedpath, ldr_loadpathpath, \
        ldr_loadpathprocess, ldr_initpathpath, ldr_initpathprocess, ldr_mempathpath, ldr_mempathprocess = line_ldrmodules

        if ldr_loadpathpath != ldr_initpathpath or ldr_loadpathpath != ldr_mempathpath or ldr_mempathpath != ldr_initpathpath:
            if ldr_ininit == 'True' and ldr_inload == 'True' and ldr_inmem == 'True':
                report += 'Non matching Paths + inmem, ininit and inload while Inload + Inmem and Ininit are True: Alert'
                report += '\n' + '*' * 120 + '\n'
                report += 'Process         : ' + ldr_process + '\n'
                report += 'Mapped Path     : ' + ldr_mappedpath + '\n'
                report += 'Base            : ' + ldr_base + '\n'
                report += 'Pid Ldrmodules  : ' + str(ldr_pid) + '\n'
                report += 'Inload          : ' + ldr_inload + '\n'
                report += 'Inload process  : ' + ldr_loadpathprocess + '\n'
                report += 'Inload path     : ' + ldr_loadpathpath + '\n'
                report += 'Ininint         : ' + ldr_ininit + '\n'
                report += 'Ininint process : ' + ldr_initpathprocess + '\n'
                report += 'Ininint path    : ' + ldr_initpathpath + '\n'
                report += 'Inmem           : ' + ldr_inmem + '\n'
                report += 'Inmem process   : ' + ldr_mempathprocess + '\n'
                report += 'Inmem path      : ' + ldr_mempathpath + '\n\n'

                # Get extra data for suspicious modules
                report_fileinfo += lobotomy_psxview(ldr_pid)
                report_fileinfo += lobotomy_build_pstree(ldr_pid)
                report_fileinfo += lobotomy_impscan(str(ldr_pid), str(ldr_base), database)
                report_fileinfo += lobotomy_malfind_info(ldr_pid, ldr_base)
    return report, report_fileinfo


def lobotomy_malfind_info(pid, base):
#########################################################################################
#########################################################################################
#   Add Malfind plugin
#########################################################################################
#########################################################################################
    report_malfind = ''
    for line_malfind in data_malfind:
        process_malfind, pid_malfind, address_malfind, vadtag_malfind, protection_malfind, \
        flags_malfind, header_malfind, body_malfind = line_malfind
        if str(pid_malfind) == str(pid) and int(address_malfind, 0) == int(base, 0):
            report_malfind += '\n\nMatch - Pid and Base: Malfind'
            report_malfind += '\n' + '*' * 120 + '\n'
            report_malfind += 'Process: ' + process_malfind
            report_malfind += '\tPid: ' + str(pid_malfind)
            report_malfind += '\tAddress: ' + address_malfind
            report_malfind += '\nVad: ' + vadtag_malfind
            report_malfind += '\tProtection: ' + protection_malfind
            report_malfind += '\n' + flags_malfind
            report_malfind += '\n' + header_malfind
            report_malfind += '\n' + body_malfind + '\n'

    return report_malfind


def ssdt_hooking(database):
#########################################################################################
#########################################################################################
# SSDT Inline Hooking
#########################################################################################

    # id	ssdt	mem1	entry	mem2	systemcall	owner	hookaddress	hookprocess
    # 977	SSDT[0]	80501b8c	0x0019	0xb240f80e	NtClose	PROCMON20.SYS
    report = ''
    data_ssdt = Lobotomy.get_databasedata('ssdt,mem1,entry,mem2,systemcall,owner,hookaddress,hookprocess', 'ssdt', database)
    for line_ssdt in data_ssdt:

# Need to build OS independed:
# Remember that the name of the NT module may not always be ntoskrnl.exe . It could
# be ntkrnlpa.exe or ntkrnlmp.exe , so make sure to adjust your regular expression
# accordingly.
# AMF page 393

        if imagetype.startswith('WinXP') and 'x86' in imagetype:
            if line_ssdt[0] == 'ssdt[0]' and \
                line_ssdt[5] != 'ntoskrnl.exe': # or \
                # line_ssdt[5] != 'ntkrnlpa.exe' or \
                # line_ssdt[5] != 'ntoskrnl.exe':
                report += 'alert: SSDT 0 hook on ntoskrnl.exe'
            if line_ssdt[0] == 'ssdt[1]' and \
                line_ssdt[5] != 'win32k.sys':
                report += 'alert: SSDT 1 hook on win32k.sys'
                pass
            if line_ssdt[6] != '':
                report += '\nSSDT        : ' + str(line_ssdt[0])
                report += '\nMem1        : ' + str(line_ssdt[1])
                report += '\nEnrty       : ' + str(line_ssdt[2])
                report += '\nMem2        : ' + str(line_ssdt[3])
                report += '\nSystemcall  : ' + str(line_ssdt[4])
                report += '\nOwner       : ' + str(line_ssdt[5])
                report += '\nHookaddress : ' + str(line_ssdt[6])
                report += '\nHookprocess : ' + str(line_ssdt[7])
                report += '\nTodo: dumping hooked process'
    return report


def lobotomy_build_pstree_old(tree_pid):
    list_pstree = []
    report_tree = ''
    for line_pstree in data_pstree:
        depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
        plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
        list_pstree.append(line_pstree)
        if str(pid_pstree) == str(tree_pid):
            report_tree += '\nTrying to build pidtree from pid to system.'
            report_tree += '\n' + '*' * 120 + '\n'
            tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
            tmpcounter = 0
            report_tree += '-' * int(depth_pstree) + ' '
            for tmplen in tmp:
                if str(tmp[tmpcounter]) == 'offset':
                    report_tree += tmp[tmpcounter] + '\t\t'
                if str(tmp[tmpcounter]) == 'name':
                    report_tree += tmp[tmpcounter] + '\t\t'
                if tmpcounter >= 2:
                    report_tree += str(tmp[tmpcounter]) + '\t'
                tmpcounter += 1
            tmpcounter = 0
            report_tree += '\n'
            report_tree += '-' * int(depth_pstree) + ' '
            for tmplen in tmp:
                if str(tmp[tmpcounter]) == 'offset':
                    report_tree += str(line_pstree[tmpcounter + 1]) + '\t\t'
                if str(tmp[tmpcounter]) == 'name':
                    report_tree += line_pstree[tmpcounter + 1] + '\t'
                if tmpcounter >= 2:
                    report_tree += str(line_pstree[tmpcounter + 1]) + '\t'

                tmpcounter += 1
            report_tree += '\n'
            report_tree += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
            report_tree += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
            report_tree += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
            tree = str(line_pstree[4])
            while tree != '0':
                tmpcounter = 0
                for tmptree in list_pstree:
                    if str(tmptree[3]) == tree:
                        report_tree += '\n' + '-' * 120 + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' '
                        for tmplen in tmp:
                            if str(tmp[tmpcounter]) == 'offset':
                                report_tree += str(tmptree[tmpcounter + 1]) + '\t\t'
                            if str(tmp[tmpcounter]) == 'name':
                                report_tree += tmptree[tmpcounter + 1] + '\t'
                                if tmptree[tmpcounter + 1] == 'System':
                                    report_tree += '\t'
                            if tmpcounter >= 2:
                                report_tree += str(tmptree[tmpcounter + 1]) + '\t'

                            tmpcounter += 1
                        report_tree += '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                        tree = str(tmptree[4])
            report_tree += '\n' + '-' * 120 + '\n'
    return report_tree


def lobotomy_build_pstree(tree_pid):
    list_pstree = []
    report_tree = ''
    counter = 0
    for line_pstree in data_pstree:
        depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
        plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
        list_pstree.append(line_pstree)
        if str(pid_pstree) == str(tree_pid):
            if report_tree == '':
                report_tree += '\nTrying to build pidtree from pid to system.'
                report_tree += '\n' + '*' * 120 + '\n'
            tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
            tmpcounter = 0
            report_tree += '-' * int(depth_pstree) + ' '
            for tmplen in tmp:
                if str(tmp[tmpcounter]) == 'offset':
                    report_tree += tmp[tmpcounter] + '\t'
                if str(tmp[tmpcounter]) == 'name':
                    report_tree += tmp[tmpcounter] + '\t\t'
                if tmpcounter >= 2:
                    report_tree += str(tmp[tmpcounter]) + '\t'
                tmpcounter += 1
            tmpcounter = 0
            report_tree += '\n'
            report_tree += '-' * int(depth_pstree) + ' '
            for tmplen in tmp:
                if str(tmp[tmpcounter]) == 'offset':
                    report_tree += str(line_pstree[tmpcounter + 1]) + '\t'
                if str(tmp[tmpcounter]) == 'name':
                    if len(line_pstree[tmpcounter + 1]) < 8:
                        report_tree += line_pstree[tmpcounter + 1] + '\t\t'
                    if len(line_pstree[tmpcounter + 1]) >= 8:
                        report_tree += line_pstree[tmpcounter + 1] + '\t'
                if tmpcounter >= 2:
                    report_tree += str(line_pstree[tmpcounter + 1]) + '\t'

                tmpcounter += 1
            report_tree += '\n'
            report_tree += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
            report_tree += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
            report_tree += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
            tree = str(line_pstree[4])
            while tree != '0':
                counter += 1
                tmpcounter = 0
                for tmptree in list_pstree:
                    if str(tmptree[3]) == tree:
                        report_tree += '\n' + '-' * 120 + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' '
                        for tmplen in tmp:
                            if str(tmp[tmpcounter]) == 'offset':
                                if line_pstree[0] < 4:
                                    report_tree += str(tmptree[tmpcounter + 1]) + '\t'
                                if line_pstree[0] >= 4:
                                    report_tree += str(tmptree[tmpcounter + 1]) + '\t'
                            if str(tmp[tmpcounter]) == 'name':
                                report_tree += tmptree[tmpcounter + 1] + '\t'
                                if tmptree[tmpcounter + 1] == 'System':
                                    report_tree += '\t'
                            if tmpcounter >= 2:
                                report_tree += str(tmptree[tmpcounter + 1]) + '\t'

                            tmpcounter += 1
                        report_tree += '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                        report_tree += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                        tree = str(tmptree[4])
                if counter == 1000:
                    report_tree += '\n\nFail to build tree to system, probably a orphan pid.\n'
                    tree = '0'
            report_tree += '\n' + '-' * 120 + '\n'
    return report_tree


def lobotomy_build_pstree_children(tree_pid):
    list_pstree = []
    report_tree = ''
    childpid = []
    tmpchildpids = []
    counter = 0
    lineheader = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
    for line_pstree in data_pstree:
        if report_tree == '':
            report_tree += '\nTrying to build pidtree to get all the children from pid.'
            report_tree += '\n' + '*' * 120 + '\n'
            report_tree += '-' * int(line_pstree[0]) + ' '

        # depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
        # plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
        if line_pstree[3] == tree_pid:
            # got the pid.
            # need to build a child list
            # set the first pid to follow
            follow_pid = tree_pid
            while counter < 5000:
            #while len(tmpchildpids) > 0:
                for line_childpid in data_pstree:
                    if line_childpid[4] == follow_pid:
                        childpid.append(line_childpid)
                        tmpchildpids.append(line_childpid[3])
                        # got the first child items
                        # need to get more childs.

                try:
                    follow_pid = tmpchildpids.pop()
                except:
                    pass
                counter += 1
    for line in childpid:
        tmpcounter = 0
        report_tree += '\n' + '-' * 120 + '\n'
        report_tree += '-' * int(line[0]) + ' '
        # Header
        for tmplen in lineheader:
            if str(lineheader[tmpcounter]) == 'offset':
                if line[0] < 5:
                    report_tree += lineheader[tmpcounter] + '\t'
                if line[0] >= 5:
                    report_tree += lineheader[tmpcounter] + '\t\t'
            if str(lineheader[tmpcounter]) == 'name':
                if line[0] < 4:
                    report_tree += lineheader[tmpcounter] + '\t\t'
                if line[0] >= 4:
                    report_tree += lineheader[tmpcounter] + '\t'
            if tmpcounter >= 2:
                report_tree += str(lineheader[tmpcounter]) + '\t'
            tmpcounter += 1
        report_tree += '\n'
        tmpcounter = 0
        report_tree += '-' * int(line[0]) + ' '
        # Body
        for tmplen in lineheader:
            if str(lineheader[tmpcounter]) == 'offset':
                if line[0] < 4:
                    report_tree += str(line[tmpcounter + 1]) + '\t\t'
                if line[0] >= 4:
                    report_tree += str(line[tmpcounter + 1]) + '\t'
            if str(lineheader[tmpcounter]) == 'name':
                if len(line[tmpcounter + 1]) < 8:
                    report_tree += line[tmpcounter + 1] + '\t\t'
                if len(line[tmpcounter + 1]) >= 8:
                    report_tree += line[tmpcounter + 1] + '\t'
                if line[tmpcounter + 1] == 'System':
                    report_tree += '\t'
            if tmpcounter >= 2:
                report_tree += str(line[tmpcounter + 1]) + '\t'

            tmpcounter += 1
        report_tree += '\n' + '-' * int(line[0]) + ' Audit : ' + line[8]
        report_tree += '\n' + '-' * int(line[0]) + ' Cmd   : ' + line[9]
        report_tree += '\n' + '-' * int(line[0]) + ' Path  : ' + line[10] + '\n'
    if len(report_tree) <= 182:
        report_tree += "\nPid doesnt have children."
    return report_tree


def lobotomy_impscan(pid, base, database):
    report = ''
    data_impscan = Lobotomy.get_databasedata('process,pid,base,iat,`call`,module,function', 'impscan', database)
    if data_impscan != None and data_impscan != '------ ERROR reading autostart! ------':
        for line_impscan in data_impscan:
            if str(line_impscan[1]) == str(pid) and str(line_impscan[2]) == str(base):
                if report == '':
                    report += '\nLobotomy Import Scan for pid:{} and base: {}'. format(pid, base)
                    report += '\n' + '*' * 120

                report += '\n{:16}{:6}{:20}{:16}{:12}{:32}{}'.format(line_impscan[0], line_impscan[1], line_impscan[2],
                                        line_impscan[3], line_impscan[4], line_impscan[5], line_impscan[6])
                #report += '\n' + str(line_impscan)
    else:
        report += '\nLobotomy Import Scan for pid:{} and base: {}'. format(pid, base)
        report += '\n' + '*' * 120
        report += '\nNo imports found for pid: {} at base: {}'.format(pid, base)
    return report


def lobotomy_exifinfo(filename):
    report_info = ''
    for line_exifinfo in data_exifinfo:
        filename_exifinfo,exifinfo = line_exifinfo
        if filename_exifinfo == filename:
            report_info += '\nMatch - Filename: Exifinfo'
            report_info += '\n' + '*' * 120 + '\n'
            report_info += 'Fullfilename:                  ' + filename_exifinfo + '\n'
            report_info += exifinfo + '\n'
    return report_info


def lobotomy_pe_scan(filename):
    report_info = ''
    for line_pe_scan in data_pe_scan:
        Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
        if Fullfilename_pe == filename:
            report_info += '\nMatch - Filename: PEScanner'
            report_info += '\n' + '*' * 120 + '\n'
            report_info += 'Fullfilename        : ' + Fullfilename_pe + '\n'
            report_info += 'PE Compile time     : ' + Pe_Compiletime + '\n'
            report_info += 'PE Packer           : ' + Pe_Packer + '\n'
            report_info += 'File type PE file   : ' + Filetype_pe + '\n'
            report_info += 'Original Filename   : ' + Original_Filename_pe + '\n'
            report_info += 'Yara Result         : ' + Yara_Results_pe + '\n' + '\n'

    for line_pe_scan_beta in data_pe_scan_beta:
        Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
        if Fullfilename_pe_beta == filename:
            report_info += '\nMatch - Filename: PE_Scan_Beta'
            report_info += '\n' + '*' * 120 + '\n'
            report_info += 'Fullfilename:       ' + Fullfilename_pe_beta + '\n'
            report_info += 'PE info:            \n' + Pe_Blob_beta + '\n\n'
    return report_info


def lobotomy_psxview(pid):
    report_fileinfo = ''
    for line_psxview in data_psxview:
        offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
        pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
        if str(pid_psxview) == str(pid):
            report_fileinfo += '\nMatch - Pid: PSXview'
            report_fileinfo += '\n' + '*' * 120 + '\n'
            tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
            tmpcounter = 0
            for tmplen in line_psxview:
                if len(str(tmp[tmpcounter])) <= 8 and len(str(line_psxview[tmpcounter])) <= 8:# or len(str(tmp[tmpcounter])) <= len(str(line_psxview[tmpcounter])):
                    report_fileinfo += tmp[tmpcounter] + '\t'
                else:
                    report_fileinfo += tmp[tmpcounter] + '\t\t'
                tmpcounter += 1
            tmpcounter = 0
            report_fileinfo += '\n'
            for tmplen in line_psxview:
                report_fileinfo += str(line_psxview[tmpcounter]) + \
                              ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                tmpcounter += 1
            report_fileinfo += '\n'
    return report_fileinfo


def lobotomy_volyarascan(pid, filename):
    report_info = ''
    for line_vol_yara in data_vol_yara:
        ownername_vol_yara, pid_vol_yara, rule_vol_yara, data_offset_vol_yara,\
        data_bytes_vol_yara, data_txt_vol_yara = line_vol_yara
        if str(pid_vol_yara) == str(pid):
            report_info += '\nMatch - Pid: volatility_Yarascan' + '\n'
            report_info += '***********************************' + '\n'
            report_info += 'Fullfilename        : ' + filename + '\n'
            report_info += 'Pid from yara       : ' + str(pid_vol_yara) + '\n'
            report_info += 'Ownername Yara      : ' + ownername_vol_yara + '\n'
            report_info += 'Ownername Yara      : ' + rule_vol_yara + '\n'
            data_offset_vol_yara = data_offset_vol_yara.split('\n')
            data_bytes_vol_yara = data_bytes_vol_yara.split('\n')
            data_txt_vol_yara = data_txt_vol_yara.split('\n')
            linenr = 0
            report_info += '=' * 88 + '\nYaradata\n' + '=' * 88
            for test in data_offset_vol_yara:
                report_info += '\n' + data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                              data_txt_vol_yara[linenr]
                linenr += 1
            report_info += '\n' + '=' * 88 + '\n'
    return report_info


def lobotomy_orphan_threadscan(database):
    report = ''
    report_thread1 = ''
    report_thread2 = ''
    pid_list = ''

# Route: threat -> psxview.
# or a better way: vol.py -f orphan.vmem threads -F OrphanThread
# If pid not in psxview, threat (pid) is orphan
# Pid can be orphan.
# id	offset	            pid	tid	    startaddress	createtime	        exittime
# 1	    0x0000000001c64990	688	1504	0x7c8106e9	    2010-10-08 03:59:59	0000-00-00 00:00:00

# id	ethread	    pid	    tid	    tags	    created	                        exited	                        owner
# 	state	blob
# 1	    0x82270808	1032	1924	HookedSSDT	2010-10-29 17:11:49 UTC+0000	1970-01-01 00:00:00 UTC+0000	svchost.exe
# Waiting:UserRequest	Volatility Foundation Volatility Framework 2.4
# [x86] Gathering all referenced SSDTs from KTHREADs...
# Finding appropriate address space for tables...

    data_threads = Lobotomy.get_databasedata('ethread,pid,tid,tags,created,exited,owner,state,`blob`', 'threads', database)
    try:
        for line_threads in data_threads:
            if 'OrphanThread' in line_threads[3]:
                if report_thread1 == '':
                    report_thread1 += '\nLooking for Orphan Thread.'
                    report_thread1 += '\nWith Volatility plugin Threads.'
                    report_thread1 += '\n' + '*' * 120
                report_thread1 += '\n' + line_threads[8] + '\n' + '-' * 25
    except TypeError:
        # When nothing is found: TypeError: 'NoneType' is not iterable
        pass

    data_threadscan = Lobotomy.get_databasedata('offset,pid,tid,startaddress,createtime,exittime', 'thrdscan', database)
    if data_threadscan != None and data_threadscan != '------ ERROR reading autostart! ------':
        for line_threadscan in data_threadscan:
            # make a list of all the pids in psxview
            for psxview_pid in data_psxview:
                pid_list += str(psxview_pid[2])
            if str(line_threadscan[1]) not in str(pid_list):
                # Build orphan thread report_thread2
                if report_thread2 == '':
                    report_thread2 += '\nLooking for Orphan Thread.'
                    report_thread2 += '\nBy comparing threadscan with psxview, looking for threads without a PID.'
                    report_thread2 += '\n' + '*' * 120
                report_thread2 += '\n\nFound Orphan Thread:'
                report_thread2 += '\nOffset      : ' + str(line_threadscan[0])
                report_thread2 += '\nPid         : ' + str(line_threadscan[1])
                report_thread2 += '\nTid         : ' + str(line_threadscan[2])
                report_thread2 += '\nStartaddress: ' + str(line_threadscan[3])
                report_thread2 += '\nCreatetime  : ' + str(line_threadscan[4])
                report_thread2 += '\nExittime    : ' + str(line_threadscan[5])
    report = report_thread1 + report_thread2
    return report


def lobotomy_msfdetect(database):
# Find Metasploit meterpreter strings in memorydump and try to link the pid with other modules.
# 1. try to find pstree (find childeren of pid)
# 2. try to find a way to get the ldrmodules and imports (impscan)


    report = ''
    report_pidinfo = ''
    # tmppidlist = []
    # tmpvpidlist = []
    tmppids = []
    tmpvpids = []
    pids = []
    nopid = []
    vpids = []
    data_msfscan = Lobotomy.get_databasedata('stringsoffset,pid,pidoffset,vpid,vpidoffset,value', 'msfdetect', database)
    # data_ldrmod = Lobotomy.get_databasedata('pid,process,base,inload,ininit,inmem,mappedpath,loadpathpath,'
    #                                         'loadpathprocess, initpathpath, initpathprocess, mempathpath,'
    #                                         'mempathprocess', 'ldrmodules_v', database)
    for line in data_msfscan:
        if line[1] != 0:
            tmppids.append(line[1])
        if line[3] != 0:
            tmpvpids.append(line[3])
        if line[2] == 'FREE MEMORY':
            nopid.append(line[3])

    # newList = list(set(oldList))
    pids = list(set(tmppids))
    vpids = list(set(tmpvpids))
    try:
        if pids[0] != '':
            report += '\nLooking for MSF strings.'
            report += '\n' + '*' * 120
            report += '\n\nFound {} items in {} pid(s)'.format(len(tmppids), len(pids))
            report += '\nFound {} items in {} possible infected pid(s)'.format(len(tmpvpids), len(vpids))
            report += '\nFound {} items without a pid'.format(len(nopid))
        for pid in pids:
            if str(pid) != '0':
                report += '\nPossible infected pid: {}'.format(str(pid))
                report_pidinfo += '\nPossible infected pid: {}'.format(str(pid))
                report_pidinfo += lobotomy_psxview(int(pid))
                report_pidinfo += lobotomy_build_pstree(int(pid))
                report_pidinfo += lobotomy_build_pstree_children(int(pid))
        for pid in vpids:
            if str(pid) != '0':
                report += '\nPossible infected targeted pid: {}'.format(str(pid))
                report_pidinfo += '\nPossible infected targeted pid: {}'.format(str(pid))
                report_pidinfo += lobotomy_psxview(int(pid))
                report_pidinfo += lobotomy_build_pstree(int(pid))
                report_pidinfo += lobotomy_build_pstree_children(int(pid))
    except IndexError:
        pass

    if report != '':
        report += '\nPlease check Lobotomy website, database {}, plugin msfdetect for more information'.format(database)

        # report_fileinfo += lobotomy_impscan(str(ldr_pid), str(ldr_base), database)
        # report_fileinfo += lobotomy_malfind_info(ldr_pid, ldr_base)

        # to soon to get ldrmodules
        # for ldr_line in data_ldrmod:
        #     if str(pid) == str(ldr_line):
        #         if report == '':
        #             report += '\nLooking for MSF Strings.'
        #             report += '\nAnd trying to find the process, modules and imports of the exploited pid.'
        #             report += '\n' + '*' * 120
        #         report += '\nProcess         : ' + ldr_process
        #         report += '\nMapped Path     : ' + ldr_mappedpath
        #         report += '\nBase            : ' + ldr_base
        #         report += '\nPid Ldrmodules  : ' + str(ldr_pid)
        #         report += '\nInload          : ' + ldr_inload
        #         report += '\nInload process  : ' + ldr_loadpathprocess
        #         report += '\nInload path     : ' + ldr_loadpathpath
        #         report += '\nIninint         : ' + ldr_ininit
        #         report += '\nIninint process : ' + ldr_initpathprocess
        #         report += '\nIninint path    : ' + ldr_initpathpath
        #         report += '\nInmem           : ' + ldr_inmem
        #         report += '\nInmem process   : ' + ldr_mempathprocess
        #         report += '\nInmem path      : ' + ldr_mempathpath + '\n'
        #
        #         # Get extra data for suspicious modules
        #         report_fileinfo += lobotomy_psxview(ldr_pid)
        #         report_fileinfo += lobotomy_build_pstree(ldr_pid)
        #         report_fileinfo += lobotomy_impscan(str(ldr_pid), str(ldr_base), database)
        #         report_fileinfo += lobotomy_malfind_info(ldr_pid, ldr_base)
    # exit()
    return report, report_pidinfo


def lobotomy_explain(explain):
    if explain == 'Malicious_Timers':
        explanation = 'Hier komt de uitleg'
        return explanation
    if explain == 'Scanned Bad Hashes':
        explanation = 'Hier komt de uitleg'
        return explanation
    if explain == 'Unlinked dlls':
        explanation = 'Hier komt de uitleg'
        return explanation
    if explain == 'Suspicious Modules':
        explanation = 'Hier komt de uitleg'
        return explanation
    if explain == 'SSDT Hooking':
        explanation = '\nBook: Art of Memory Forensics, page 394:'
        explanation += '\nInline Hooking'
        explanation += '\nAttackers are well aware of the methods used to detect the modifications their tools'
        explanation += '\nmake to systems. Thus, instead of pointing SSDT functions outside of the NT module or'
        explanation += '\nwin32ks.sys, they can just use an inline hooking technique. This technique has the same'
        explanation += '\neffect of redirecting execution to a malicious function, but it is not as obvious. Here’s an'
        explanation += '\nexample of how it appeared when the Skynet rootkit hooked NtEnumerateKey(we added '
        explanation += '\nthe --verboseflag to check for these inline hooks):'
        explanation += '\n$ python vol.py -f skynet.bin --profile=WinXPSP3x86 ssdt --verbose'
        explanation += '\n[snip]'
        explanation += '\nSSDT[0] at 804e26a8 with 284 entries'
        explanation += '\nEntry 0x0047: 0x80570d64 (NtEnumerateKey) owned by ntoskrnl.exe'
        explanation += '\n** INLINE HOOK? => 0x820f1b3c (UNKNOWN)'
        explanation += '\nEntry 0x0048: 0x80648aeb (NtEnumerateSystem[snip]) owned by ntoskrnl.exe'
        explanation += '\nEntry 0x0049: 0x80590677 (NtEnumerateValueKey) owned by ntoskrnl.exe'
        explanation += '\nEntry 0x004a: 0x80625738 (NtExtendSection) owned by ntoskrnl.exe'
        explanation += '\nEntry 0x004b: 0x805b0b4e (NtFilterToken) owned by ntoskrnl.exe'
        explanation += '\nEntry 0x004c: 0x805899b4 (NtFindAtom) owned by ntoskrnl.exe'
        explanation += '\nThe pointer 0x80570d64is indeed owned by ntoskrnl.exe, but the instructions at that'
        explanation += '\naddress have been overwritten with a JMP that leads to 0x820f1b3c.'
        explanation += '\n\nExtra resource:'
        explanation += '\nhttp://resources.infosecinstitute.com/hooking-system-service-dispatch-table-ssdt/'
        return explanation
    if explain == 'Orphan thread':
        explanation = 'Hier komt de uitleg'
        return explanation


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <database>"
    else:
        main(sys.argv[1])




#
#
#       Todo
#
#

exit()
#########################################################################################
#########################################################################################
#
#   ClamAV Scan
#########################################################################################
#########################################################################################
    # cprint += '\n***********************************' + '\n'
    # cprint += 'ClamAV findings'
    # cprint += '\n***********************************' + '\n'
    # for line_pe_scan_beta in data_pe_scan_beta:
    #     pe_scan_beta_filename, pe_scan_beta_pe_blob = line_pe_scan_beta
    #     tmp_pe_scan_beta_pe_blob = pe_scan_beta_pe_blob.split('\n')
    #     for test_clam in tmp_pe_scan_beta_pe_blob:
    #         if 'Clamav' in test_clam:
    #             clam_line = test_clam.split(':')
    #             if clam_line[0] == 'Clamav' and clam_line[2].strip(' ') != 'OK':
    #                 for item in clam_line:
    #                     cprint += item + '\t'
    #                 cprint += '\n'
    #                 cprint += pe_scan_beta_pe_blob + '\n'
    #
    #
    #
    #
    # print '\n\n#########################################################################################'
    # print '#########################################################################################'
    # print '# Dumping Suspicious Processes'
    # print '#########################################################################################'
    #
    # #data_psscan = Lobotomy.get_databasedata('offset,name,pid,ppid,pdb,timecreated,timeexited', 'psscan', database)
    # data_pslist = Lobotomy.get_databasedata('offset,name,pid,ppid,thds,hnds,sess,wow64', 'pslist', database)
    # tmp = ''
    # tmpcounter = 0
    # a = ''
    # for line_pslist in data_pslist:
    #     # Add all processes from pslist in a string
    #     tmp += str(line_pslist[1]) + ' '
    #
    # for line_psxview in data_psxview:
    #     # test if process from psxview does not match data from pslist and if exittime doesn't have a value
    #     if line_psxview[1] not in tmp and line_psxview[10] == None:
    #         print 'error', line_psxview



# Putting It All Together
# Now that you’ve been exposed to the various methods of finding and analyzing malicious
# code in the kernel, we’ll show you an example of how to put all the pieces together. In
# this case, we first noticed the rootkit’s presence due to its timers and callbacks that point
# into memory that isn’t owned by a module in the loaded module list. Here is the relevant
# output from those two plugins:
# $ python vol.py -f spark.mem --profile=WinXPSP3x86 timers
# Volatility Foundation Volatility Framework 2.4
# Offset(V)     DueTime                     Period(ms)  Signaled    Routine     Module
# ----------    ------------------------    ----------  --------    ----------  ------
# 0x8055b200    0x00000086:0x1c631c38       0           -           0x80534a2a  ntoskrnl.exe
# 0x805516d0    0x00000083:0xe04693bc       60000       Yes         0x804f3eae  ntoskrnl.exe
# 0x81dc52a0    0x00000083:0xe2d175b6       60000       Yes         0xf83fb6bc  NDIS.sys
# 0x81eb8e28    0x00000083:0xd94cd26a       0           -           0x80534e48  ntoskrnl.exe
# [snip]
# 0x80550ce0    0x00000083:0xc731f6fa       0           -           0x8053b8fc  ntoskrnl.exe
# 0x81b9f790    0x00000084:0x290c9ad8       60000       -           0x81b99db0  UNKNOWN
# 0x822771a0    0x00000131:0x2e8701a8       0           -           0xf83faf6f  NDIS.sys

# $ python vol.py -f spark.mem --profile=WinXPSP3x86 callbacks
# Volatility Foundation Volatility Framework 2.4
# Type                              Callback   Module       Details
# --------------------------------- ---------- -----------  -------
# IoRegisterFsRegistrationChange    0xf84be876 sr.sys       -
# KeBugCheckCallbackListHead        0xf83e65ef NDIS.sys     Ndis miniport
# KeBugCheckCallbackListHead        0x806d77cc hal.dll      ACPI 1.0 - APIC
# IoRegisterShutdownNotification    0x81b934e0 UNKNOWN      \Driver\03621276
# IoRegisterShutdownNotification    0xf88ddc74 Cdfs.SYS     \FileSystem\Cdfs
# [snip]
# PsSetCreateProcessNotifyRoutine   0xf87ad194 vmci.sys     -
# CmRegisterCallback                0x81b92d60 UNKNOWN      -

# A procedure at 0x81b99db0 is set to execute every 60,000 milliseconds, a function at
# 0x81b934e0 is set to call when the system shuts down, and a function at 0x81b92d60 gets
# notified of all registry operations. This rootkit has clearly “planted some seeds” into the
# kernel of this victim system. At this point, you don’t know the name of its module, but you
# can see that the shutdown callback is associated with a driver named \Driver\03621276 .
# Given that information, you can seek more details with the driverscan plugin:
#
# $ python vol.py -f spark.mem --profile=WinXPSP3x86 driverscan
# Volatility Foundation Volatility Framework 2.4

# Offset(P)     Ptr     Start       Size        ServiceKey          Driver Name
# ----------    ----    ----------  --------    -----------------   -----------
# 0x01e109b8    1       0x00000000  0x0         \Driver\03621276    \Driver\03621276
# 0x0214f4c8    1       0x00000000  0x0         \Driver\03621275    \Driver\03621275
# [snip]
#
# Kernel Forensics and Rootkits
# According to this output, the starting address for the kernel module that created the
# suspect driver object is zero. It could be an anti-forensics technique to prevent analysts
# from dumping the malicious code. Indeed, it is working so far because to extract the
# module, you either need the module’s name or base address, and you already know that
# the name is not available. However, there are various pointers inside the malicious mod-
# ule’s code; you just need to find out where the PE file starts. You can do this with a little
# scripting inside volshell , using one of the following techniques:
# •	 Take one of the addresses and scan backward looking for a valid MZ signature.
# If the malicious PE file has several other binaries embedded, the first result might
# not be the right one.
# •	 Set your starting address somewhere between 20KB and 1MB behind the lowest
# pointer that you have; then walk forward looking for a valid MZ signature.
# The following code shows how to perform the second method:
# $ python vol.py -f spark.mem volshell
# [snip]
# >>> start = 0x81b99db0 - 0x100000
# >>> end = 0x81b93690
# >>> while start < end:
# ...
# if addrspace().zread(start, 4) == "MZ\x90\x00":
# ...
# print hex(start)
# ...
# break
# ...
# start += 1
# ...
# 0x81b91b80
# NOTE
# Alternatively, you can translate the virtual address into a physical offset by calling the
# addrspace().vtop(ADDR) function. Provided you have a raw, padded memory dump,
# you can open it in a hex editor and seek to the physical offset—then scroll up to find
# the MZ signature.
# You found an MZ signature at 0x81b91b80 , which is about 8KB above the timers and
# callbacks procedures. You can also verify the PE header in volshell :
# >>> db(0x81b91b80)
# 0x81b91b80 4d5a 9000 0300 0000 0400 0000 ffff 0000
# 0x81b91b90 b800 0000 0000 0000 4000 0000 0000 0000
# 0x81b91ba0 0000 0000 0000 0000 0000 0000 0000 0000
# MZ..............
# ........@.......
# ................
# 403404 Part II: Windows Memory Forensics
# 0x81b91bb0
# 0x81b91bc0
# 0x81b91bd0
# 0x81b91be0
# 0x81b91bf0
# 0000
# 0e1f
# 6973
# 7420
# 6d6f
# 0000
# ba0e
# 2070
# 6265
# 6465
# 0000
# 00b4
# 726f
# 2072
# 2e0d
# 0000
# 09cd
# 6772
# 756e
# 0d0a
# 0000
# 21b8
# 616d
# 2069
# 2400
# 0000
# 014c
# 2063
# 6e20
# 0000
# d000
# cd21
# 616e
# 444f
# 0000
# 0000
# 5468
# 6e6f
# 5320
# 0000
# ................
# ........!..L.!Th
# is.program.canno
# t.be.run.in.DOS.
# mode....$.......
# Finally, you can now supply a base address to the moddump plugin and extract the
# module from memory:
# $ python vol.py -f spark.mem moddump -b 0x81b91b80 --dump-dir=OUTPUT
# --profile=WinXPSP3x86
# Volatility Foundation Volatility Framework 2.4
# Module Base Module Name
# Result
# ----------- -------------------- ------
# 0x081b91b80 UNKNOWN
# OK: driver.81b91b80.sys
# You have to fix the ImageBase value in the PE header to match where you found it:
# $ python
# Python 2.7.6 (v2.7.6:3a1db0d2747e, Nov 10 2013, 00:42:54)
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import pefile
# >>> pe = pefile.PE("driver.81b91b80.sys")
# >>> pe.OPTIONAL_HEADER.ImageBase = 0x81b91b80
# >>> pe.write("driver.81b91b80.sys")




#########################################################################################
#########################################################################################
# Dumping Suspicious Kernel Modules
#########################################################################################

# id	offset	name	base	size	file
# 120	0x82258ad0	PROCMON20.SYS	0xb240b000	0xc000	\\??\\C:\\WINDOWS\\system32\\Drivers\\PROCMON20.SYS
# 121	0x81f8cb60	mrxcls.sys	0xf895a000	0x5000	\\??\\C:\\WINDOWS\\system32\\Drivers\\mrxcls.sys
# 122	0x81c2a530	mrxnet.sys	0xb21d8000	0x3000	\\??\\C:\\WINDOWS\\system32\\Drivers\\mrxnet.sys


# The modules command in Volatility prints a list of loaded kernel modules by walking
# the list of LDR_DATA_TABLE_ENTRY structures. Because of the nature of the doubly linked list,
# it is possible for malware to unlink entries and hide drivers. However, just as psscan (see
# Recipe 15-6) provides you with the capability to detect unlinked processes, the modscan2
# command gives you the power to detect unlinked kernel modules. Just compare the output
# between modules and modscan2 and see if there are any discrepancies.

#
# PSScan - PSXView (where exittime is 0)

# psxview
# id	offset	    name	        pid	    pslist	psscan	thrdproc	pspcid	csrss	session	deskthrd	exittime
# 14	0x0113f648	1_doc_RCData_61	1336	False	True	True	    True	True	True	True	    0000-00-00 00:00:00
#
# psscan
# id	offset	            name	        pid	    ppid	pdb	        timecreated	        timeexited
# 4	    0x000000000113f648	1_doc_RCData_61	1336	1136	0x06cc0340	2010-08-11 16:50:20	0000-00-00 00:00:00
# 10	0x0000000004a544b0	ImmunityDebugge	1136	1724	0x06cc02a0	2010-08-11 16:50:19	0000-00-00 00:00:00
#
# pslist
# id	offset	    name	pid	ppid	thds	hnds	sess	wow64	start	            exit
# 1	    0x810b1660	System	4	0	    56	    253	    0	    0	    0000-00-00 00:00:00	0000-00-00 00:00:00
# id	offset	name	pid	ppid	thds	hnds	sess	wow64	start	exit
# 1	0x810b1660	System	4	0	56	253	0	0	0000-00-00 00:00:00	0000-00-00 00:00:00
#
# pstree
# id	depth	offset	    name	    pid	    ppid	thds	hnds	plugin_time	        audit	cmd	path
# 18	4	    0xff203b80	svchost.exe	1148	676	    14	    207	    2010-08-11 06:06:26	\\Device\\HarddiskVolume1\\WINDOWS\\system32\\svchost.exe



    # for line_pslist in data_pslist:
    #     tmp = 0
    #     for tmpdata in data_psxview:
    #         a += tmpdata[1] + ' '
    #         print a
    #     if line_pslist[1] not in a:
    #         print 'error', tmpcounter, line_pslist
    #         tmpcounter += 1
    #     for line_psxview in data_psxview:
    #
    #         #print line_psxview[1], line_psscan[1]
    #         if line_psxview[1] == line_pslist[1]:
    #             tmp = 1
    #             print 'same: ', line_psxview[1], line_pslist[1]
    #             # process name from psxview is processname from psscan
    #             # ok
    #     if tmp == 0:
    #         print line_pslist
    #         print line_psxview
    #         tmp = 0
    #         # if line_psscan[1] not in data_psxview:
    #         #     print line_psscan


# Need to build OS independed:
# Remember that the name of the NT module may not always be ntoskrnl.exe . It could
# be ntkrnlpa.exe or ntkrnlmp.exe , so make sure to adjust your regular expression
# accordingly.
# AMF page 393

        # if imagetype.startswith('WinXP') and 'x86' in imagetype:
        #     if line_ssdt[0] == 'ssdt[0]' and \
        #         line_ssdt[5] != 'ntoskrnl.exe': # or \
        #         # line_ssdt[5] != 'ntkrnlpa.exe' or \
        #         # line_ssdt[5] != 'ntoskrnl.exe':
        #         print 'alert: ssdt 0 hook'
        #     if line_ssdt[0] == 'ssdt[1]' and \
        #         line_ssdt[5] != 'win32k.sys':
        #         print 'alert: ssdt 1 hook'
        #         pass
        #     if line_ssdt[6] != '':
        #         print line_ssdt[6], line_ssdt[7]
        #         print 'alert: ssdt hook'
        #         print line_ssdt
        #         print 'next step: dumping hooked process'





# Remember that the name of the NT module may not always be ntoskrnl.exe . It could
# be ntkrnlpa.exe or ntkrnlmp.exe , so make sure to adjust your regular expression
# accordingly.
# $ python vol.py -f laqma.vmem ssdt --profile=WinXPSP3x86
# | egrep -v '(ntoskrnl\.exe|win32k\.sys)'
# Volatility Foundation Volatility Framework 2.4
# [x86] Gathering all referenced SSDTs from KTHREADs...
# 393394 Part II: Windows Memory Forensics
# Finding appropriate address space for tables...
# SSDT[0]
# Entry
# Entry
# Entry
# Entry
# at 805011fc with 284 entries
# 0x0049: 0xf8c52884 (NtEnumerateValueKey) owned by lanmandrv.sys
# 0x007a: 0xf8c5253e (NtOpenProcess) owned by lanmandrv.sys
# 0x0091: 0xf8c52654 (NtQueryDirectoryFile) owned by lanmandrv.sys
# 0x00ad: 0xf8c52544 (NtQuerySystemInformation) owned by lanmandrv.sys
# The rootkit hooks four functions: NtEnumerateValueKey for hiding registry val-
# ues, NtOpenProcess and NtQuerySystemInformation for hiding active processes, and
# NtQueryDirectoryFile for hiding files on disk. Despite the somewhat misleading name
# ( lanmandrv.sys sounds like it could be a legitimate component), it stands out because it
# should not be handling APIs that are typically implemented by the NT module.
# Inline Hooking
# Attackers are well aware of the methods used to detect the modifications their tools
# make to systems. Thus, instead of pointing SSDT functions outside of the NT module or
# win32ks.sys , they can just use an inline hooking technique. This technique has the same
# effect of redirecting execution to a malicious function, but it is not as obvious. Here’s an
# example of how it appeared when the Skynet rootkit hooked NtEnumerateKey (we added
# the --verbose flag to check for these inline hooks):
# $ python vol.py -f skynet.bin --profile=WinXPSP3x86 ssdt --verbose
# [snip]
# SSDT[0] at 804e26a8 with 284 entries
# Entry 0x0047: 0x80570d64 (NtEnumerateKey) owned by ntoskrnl.exe
# ** INLINE HOOK? => 0x820f1b3c (UNKNOWN)
# Entry 0x0048: 0x80648aeb (NtEnumerateSystem[snip]) owned by ntoskrnl.exe
# Entry 0x0049: 0x80590677 (NtEnumerateValueKey) owned by ntoskrnl.exe
# Entry 0x004a: 0x80625738 (NtExtendSection) owned by ntoskrnl.exe
# Entry 0x004b: 0x805b0b4e (NtFilterToken) owned by ntoskrnl.exe
# Entry 0x004c: 0x805899b4 (NtFindAtom) owned by ntoskrnl.exe
# The pointer 0x80570d64 is indeed owned by ntoskrnl.exe , but the instructions at that
# address have been overwritten with a JMP that leads to 0x820f1b3c . Thus, if you check
# only the initial owning module, you’ll miss the fact that this malware hooks the SSDT.









#
#   - If Process in Mappedpath and Ininit = false, ignore.
#   - (Art of memory forensics, page 238, you never find the process exe in the init order list.)

#
#
# data_pe_scan_beta = Lobotomy.get_databasedata('Filename,Pe_Blob', 'pe_scanner_beta', database)

# To do:
#   Get list from psxview or/and psscan and get offset. use this offset to carv exe hiding from active proc list.
#   - (Art of memory forensics, page 243)

#########################################################################################
#########################################################################################
#   Done
#   volatility moddump. (we have procdump and dlldump)
#########################################################################################
#########################################################################################


#   volatility mallfind, (we use it later here, Art of memory forensics, page 254)
#   volatility vadinfo, (we use it later here, Art of memory forensics, page 260)
#
#
#
#
#
#
#   Compare ldrmodules -v (option -v) with path(s) from loaded dll's.
#
#
# vadinfo:
#
#
# VAD node @ 0x81ff1458 Start 0x00e50000 End 0x00ea9fff Tag Vad
# VAD node @ 0x820935a0 Start 0x7ffde000 End 0x7ffdefff Tag Vadl
# VAD node @ 0x82381188 Start 0x002b0000 End 0x002effff Tag VadS
#
# VadS
# Flags: CommitCharge: 4, PrivateMemory: 1, Protection: 4
# Protection: PAGE_READWRITE
#
# VadL
# Flags: CommitCharge: 1, MemCommit: 1, NoChange: 1, PrivateMemory: 1, Protection: 4
# Protection: PAGE_READWRITE
# First prototype PTE: 00000000 Last contiguous PTE: 00003a00
# Flags2: LongVad: 1, OneSecured: 1
#
# Vad
# Flags: CommitCharge: 5, ImageMap: 1, Protection: 7
# Protection: PAGE_EXECUTE_WRITECOPY
# ControlArea @823c72d8 Segment e157a008
# NumberOfSectionReferences:          1 NumberOfPfnReferences:         131
# NumberOfMappedViews:               29 NumberOfUserReferences:         30
# Control Flags: Accessed: 1, DebugSymbolsLoaded: 1, File: 1, HadUserReference: 1, Image: 1
# FileObject @823df198, Name: \Device\HarddiskVolume1\WINDOWS\system32\ntdll.dll
# First prototype PTE: e157a048 Last contiguous PTE: fffffffc
# Flags2: Inherit: 1
#
# All:
# Firstline: 	flag
# Second line: 	Protection
#
# if Vad:
# Incl FileObject and Name and
#
# Rest BLOB in DB
#
# Protection:
# if Protection == PAGE_EXECUTE_WRITECOPY
# if Protection == PAGE_EXECUTE_READWRITE
#
#
# LDRmodules uses VADINFO to build lilst. No need to compare vadinfo with ldrmodules. Source: Art of memory forensics:
# As an alternative to the multiple steps you just saw, you can also skip straight to ldrmodules.
# Remember that the process executable is added to the load order and memory
# order module lists in the PEB. Thus, when ldrmodules cross-references the information
# with the memory-mapped files in the VAD, you see a discrepancy.
#
# ldrmodules
# SELECT * FROM `ldrmodules_v` WHERE pid = '868' OR pid = '1928';
# id	pid	process	base	inload	ininit	inmem	mappedpath	loadpath	loadpathpath	loadpathprocess	initpath	initpathpath	initpathprocess	mempath	mempathpath	mempathprocess
# 1103	868	lsass.exe	0x01000000	True	False	True		Load Path	C:\\WINDOWS\\system32\\lsass.exe	lsass.exe				Mem Path	C:\\WINDOWS\\system32\\lsass.exe	lsass.exe
#
# dlllist
# SELECT * FROM `dlllist` WHERE pid = '868' OR pid = '1928';
# id	process	pid	cmd	servicepack	base	size	loadcount	dllpath
# 1218	lsass.exe	868	"C:\\WINDOWS\\\\system32\\\\lsass.exe"	Service Pack 3
# 	0x01000000	0x6000	0xffff	C:\\WINDOWS\\system32\\lsass.exe
#
# # DLLpath from pid 868 (Same base adress) and ldrmodules (ininit) does not match. Process hollowing.
# Vadinfo give us:
# Pid:    868
# VAD node @ 0x81f1ef08 Start 0x01000000 End 0x01005fff Tag Vad
# Flags: CommitCharge: 2, Protection: 6
# Protection:
# PAGE_EXECUTE_READWRITE
# ControlArea @81fbeee0 Segment e24b4c10
# NumberOfSectionReferences:          1 NumberOfPfnReferences:           0
# NumberOfMappedViews:                1 NumberOfUserReferences:          2
# Control Flags: Commit: 1, HadUserReference: 1
# First prototype PTE: e24b4c50 Last contiguous PTE: e24b4c78
# Flags2: Inherit: 1
#
# Because lsass.exe was unmapped, a name is no longer associated with the region at 0x01000000.
# But calling NtUnmapViewOfSection (step 3) doesn’t cause the PEB to lose its
# metadata, so those structures still have a record of the original mapping in the load order
# and memory order lists.


#   Bron:   volatility-yara
#           ownername
#           PID




    #Lobotomy.plugin_stop(plugin, database)
    #Lobotomy.plugin_pct(plugin, database, 100)


    #print line_print

