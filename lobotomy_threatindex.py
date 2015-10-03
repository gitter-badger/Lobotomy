# coding=utf-8
__author__ = 'Wim Venhuizen'

#
# Script version    0.6
# Plugin version:   1
# 08 mrt 2015:      Wim Venhuizen
# Plugin:           Lobotomy threat scanner
#
# Eerste opzet voor threatindex
#
# Date:             08-07-2015
# Script haalt niet meer de hele lijst met hashes op, maar controleerd in de database of een hash bestaat.
#
# 03 sep 2015:      Wim Venhuizen
#  Detail:          Added: moddump
#                   Change: Better output
# 05 sep 2015:      Wim Venhuizen
#  Detail:          Change: More volatility Yara output
#                   Add: Check pid in psxview
#                   Add: Display if ClamAV gives other then 'OK' on scanned files
# 06 sep 2015:      Wim Venhuizen
#  Detail:          Change: Minor fixes in output
#                   Add: Build pstree from pid: Note: Not sure what happens if the pid tree is broken.
#                   Change: Changed output filename to [image]-threatreport.txt
# 06 sep 2015:      Wim Venhuizen
#  Detail:          Change: Minor fixes in output
#                   Add: Build pstree from pid: Note: Not sure what happens if the pid tree is broken.
#                   Change: Changed output filename to [image]-threatreport.txt
# Name:             W Venhuizen
# Edit:             17 sep 2015
# Detail:           Add: Save report to database in table: lobotomy_report

import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()
plugin = "threatreport"
DEBUG = False


def main(database):
    Lobotomy.plugin_start('lobotomy_report', database)
    Lobotomy.plugin_pct('lobotomy_report', database, 1)

    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]


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

    starttime = time.time()
    sprint = ''
    cprint = ''
    lprintstart = ''
    lprintstart = 'Reading Database, please wait\n'
    lprintstart += 'start-time: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n'

    # Read database
    #bad_hashes = Lobotomy.get_databasedata('md5hash,added', 'bad_hashes', 'lobotomy')
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
    stoptime = time.time()
    lprintstart += 'seconds to read database(s)' +str(round(stoptime - starttime)) + '\n'
    starttime = time.time()
    lprintstart += 'stop-time: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n'
    lprintstart += 'Comparing bad_hashed with hashes from image, please wait.' + '\n'
    lprint = lprintstart
    print lprintstart
    sprint += lprintstart
    
    # Compare the hash from ddldump, procdump and photorec with the hashes in the database, bad_hashes
    # if there is no match, there will be no trigger for the program to collect data.

    lprintdlldump = ''
    for line_dlldump in data_dlldump:
        fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = line_dlldump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_dlldump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_dlldump:
                    lprintdlldump += '\n***********************************' + '\n'
                    lprintdlldump += 'Match - Volatility plugin: Dlldump. ' + '\n'
                    lprintdlldump += 'Reason match - Table Bad_hashes' + '\n'
                    lprintdlldump += '***********************************' + '\n'
                    lprintdlldump += 'Hash     : ' + md5hash_dlldump + '\n'
                    lprintdlldump += 'Filename : ' + filename_dlldump + '\n'
                    lprintdlldump += 'Module   : ' + modulename_dlldump + '\n' + '\n'
                    bad_hashes_list.append(['dlldump', fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump])
    lprint += lprintdlldump
    print lprintdlldump
    sprint += lprintdlldump

    lprintmoddump = ''
    for line_moddump in data_moddump:
        fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump, modulebase_moddump = line_moddump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_moddump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_moddump:
                    lprintmoddump += '\n***********************************' + '\n'
                    lprintmoddump += 'Match - Volatility plugin: Moddump. ' + '\n'
                    lprintmoddump += 'Reason match - Table Bad_hashes' + '\n'
                    lprintmoddump += '***********************************' + '\n'
                    lprintmoddump += 'Hash     : ' + md5hash_moddump + '\n'
                    lprintmoddump += 'Filename : ' + filename_moddump + '\n'
                    lprintmoddump += 'Base     : ' + modulebase_moddump + '\n'
                    lprintmoddump += 'Module   : ' + modulename_moddump + '\n' + '\n'
                    bad_hashes_list.append(['moddump', fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump, modulebase_moddump])
    lprint += lprintmoddump
    print lprintmoddump
    sprint += lprintmoddump

    lprintprocdump = ''
    for line_procdump in data_procdump:
        fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = line_procdump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_procdump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_procdump:
                    lprintprocdump += '\n***********************************' + '\n'
                    lprintprocdump += 'Match - Volatility plugin: Procdump. ' + '\n'
                    lprintprocdump += 'Reason match - Table Bad_hashes' + '\n'
                    lprintprocdump += '***********************************' + '\n'
                    lprintprocdump += 'Hash     : ' + md5hash_procdump + '\n'
                    lprintprocdump += 'Filename : ' + filename_procdump + '\n'
                    lprintprocdump += 'Name     : ' + name_procdump + '\n' + '\n'
                    bad_hashes_list.append(['procdump', fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump])
    lprint += lprintprocdump
    print lprintprocdump
    sprint += lprintprocdump

    lprintphoto = ''
    for line_photorec in data_photorec:
        fullfilename_photorec, md5hash_photorec = line_photorec
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_photorec.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_photorec:
                    lprintphoto += '\n***********************************' + '\n'
                    lprintphoto += 'Match - Lobotomy plugin: Photorec. ' + '\n'
                    lprintphoto += 'Reason match - Table Bad_hashes' + '\n'
                    lprintphoto += '***********************************' + '\n'
                    lprintphoto += 'Hash     : ' + md5hash_photorec + '\n'
                    lprintphoto += 'Filename : ' + fullfilename_photorec + '\n' + '\n'
                    bad_hashes_list.append(['photorec', fullfilename_photorec, md5hash_photorec])
    lprint += lprintphoto
    print lprintphoto
    sprint += lprintphoto

    stoptime = time.time()
    lprint += 'seconds to compare hashes database(s)' + str(round(stoptime - starttime)) + '\n\n'
    lprint += '***********************************\n***********************************\n\n'

    # Collect data where dlldump is the source (md5).

    line_print = ''
    for item in bad_hashes_list:
        if item[0] == 'dlldump':
            a, fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = item
            pid_dlldump = filename_dlldump.split('.')[1]
            line_print += '\n***********************************\n'
            line_print += 'collecting info for file : ' + fullfilename_dlldump + '\n'
            line_print += 'Name from dlldump        : ' + modulename_dlldump + '\n'
            line_print += 'Filename from dlldump    : ' + filename_dlldump + '\n'
            line_print += 'MD5 Hash from dlldump    : ' + md5hash_dlldump + '\n'
            line_print += 'Pid from dlldump         : ' + pid_dlldump + '\n'
            line_print += '***********************************\n' + '\n'

            for line_psxview in data_psxview:
                offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
                pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
                if str(pid_psxview) == str(pid_dlldump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Match - Pid from PSXview vs Dlldump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
                    tmpcounter = 0
                    for tmplen in line_psxview:
                        if len(str(tmp[tmpcounter])) < len(str(line_psxview[tmpcounter])):
                            line_print += tmp[tmpcounter] + '\t\t'
                        else:
                            line_print += tmp[tmpcounter] + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    for tmplen in line_psxview:
                        line_print += str(line_psxview[tmpcounter]) + \
                                      ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                        tmpcounter += 1
                    line_print += '\n'

            list_pstree = []
            for line_pstree in data_pstree:
                depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
                plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
                list_pstree.append(line_pstree)
                if str(pid_pstree) == str(pid_dlldump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Build pidtree - Pid from PSTree vs Dlldump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
                    tmpcounter = 0
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if tmpcounter >= 2:
                            line_print += str(tmp[tmpcounter]) + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += line_pstree[tmpcounter + 1] + '\t'
                        if tmpcounter >= 2:
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t'

                        tmpcounter += 1
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
                    tree = str(line_pstree[4])
                    while tree != '0':
                        tmpcounter = 0
                        for tmptree in list_pstree:
                            #line_print += str(tmptree[4]) + '\t' + str(line_pstree[3]) + '\n'
                            # pid  = 3
                            # ppid = 4
                            #if str(tmptree[4]) != '0':
                            if str(tmptree[3]) == tree:
                                line_print += '\n' + '-' * 120 + '\n'
                                line_print += '-' * int(tmptree[0]) + ' '
                                for tmplen in tmp:
                                    if str(tmp[tmpcounter]) == 'offset':
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t\t'
                                    if str(tmp[tmpcounter]) == 'name':
                                        line_print += tmptree[tmpcounter + 1] + '\t'
                                        if tmptree[tmpcounter + 1] == 'System':
                                            line_print += '\t'

                                    if tmpcounter >= 2:
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t'

                                    tmpcounter += 1
                                line_print += '\n'
                                line_print += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                                tree = str(tmptree[4])
            line_print += '\n' + '*' * 120 + '\n'

            for line_vol_yara in data_vol_yara:
                ownername_vol_yara, pid_vol_yara, rule_vol_yara, data_offset_vol_yara,\
                data_bytes_vol_yara, data_txt_vol_yara = line_vol_yara
                if str(pid_vol_yara) == str(pid_dlldump):
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - DLLDump vs volatility_Yara' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + fullfilename_dlldump + '\n'
                    line_print += 'Module              : ' + modulename_dlldump + '\n'
                    line_print += 'Filename            : ' + filename_dlldump + '\n'
                    line_print += 'Pid from dlldump    : ' + pid_dlldump + '\n'
                    line_print += 'Pid from yara       : ' + str(pid_vol_yara) + '\n'
                    line_print += 'Ownername from yara : ' + ownername_vol_yara + '\n' + '\n'
                    data_offset_vol_yara = data_offset_vol_yara.split('\n')
                    data_bytes_vol_yara = data_bytes_vol_yara.split('\n')
                    data_txt_vol_yara = data_txt_vol_yara.split('\n')
                    linenr = 0
                    line_print += '=' * 88 + '\nYaradata\n' + '=' * 88
                    for test in data_offset_vol_yara:
                        line_print += '\n' + data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr]
                        linenr += 1
                    line_print += '\n' + '=' * 88 + '\n'

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_dlldump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - DLLDump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n'

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_dlldump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - DLLDump vs PE_Scan' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe + '\n'
                    line_print += 'PE Compile time     : ' + Pe_Compiletime + '\n'
                    line_print += 'PE Packer           : ' + Pe_Packer + '\n'
                    line_print += 'File type PE file   : ' + Filetype_pe + '\n'
                    line_print += 'Original Filename   : ' + Original_Filename_pe + '\n'
                    line_print += 'Yara Result         : ' + Yara_Results_pe + '\n' + '\n'

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_dlldump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - DLLDump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n' + '\n'

        # Collect data where procdump is the source (md5).

        if item[0] == 'procdump':
            a, fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = item
            pid_procdump = filename_procdump.split('.')[1]
            line_print += '\n***********************************' + '\n'
            line_print += 'collecting info for file : ' + fullfilename_procdump + '\n'
            line_print += 'Name from procdump       : ' + name_procdump + '\n'
            line_print += 'Filename from procdump   : ' + filename_procdump + '\n'
            line_print += 'MD5 Hash from procdump   : ' + md5hash_procdump + '\n'
            line_print += 'Pid from procdump        : ' + pid_procdump + '\n'
            line_print += '***********************************\n' + '\n'

            for line_psxview in data_psxview:
                offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
                pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
                if str(pid_psxview) == str(pid_procdump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Match - Pid from PSXview vs Procdump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
                    tmpcounter = 0
                    for tmplen in line_psxview:
                        if len(str(tmp[tmpcounter])) < len(str(line_psxview[tmpcounter])):
                            line_print += tmp[tmpcounter] + '\t\t'
                        else:
                            line_print += tmp[tmpcounter] + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    for tmplen in line_psxview:
                        line_print += str(line_psxview[tmpcounter]) + \
                                      ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                        tmpcounter += 1
                    line_print += '\n'

            list_pstree = []
            for line_pstree in data_pstree:
                depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
                plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
                list_pstree.append(line_pstree)
                if str(pid_pstree) == str(pid_procdump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Build pidtree - Pid from PSTree vs Procdump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
                    tmpcounter = 0
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if tmpcounter >= 2:
                            line_print += str(tmp[tmpcounter]) + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += line_pstree[tmpcounter + 1] + '\t'
                        if tmpcounter >= 2:
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t'

                        tmpcounter += 1
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
                    tree = str(line_pstree[4])
                    while tree != '0':
                        tmpcounter = 0
                        for tmptree in list_pstree:
                            #line_print += str(tmptree[4]) + '\t' + str(line_pstree[3]) + '\n'
                            # pid  = 3
                            # ppid = 4
                            #if str(tmptree[4]) != '0':
                            if str(tmptree[3]) == tree:
                                line_print += '\n' + '-' * 120 + '\n'
                                line_print += '-' * int(tmptree[0]) + ' '
                                for tmplen in tmp:
                                    if str(tmp[tmpcounter]) == 'offset':
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t\t'
                                    if str(tmp[tmpcounter]) == 'name':
                                        line_print += tmptree[tmpcounter + 1] + '\t'
                                        if tmptree[tmpcounter + 1] == 'System':
                                            line_print += '\t'
                                    if tmpcounter >= 2:
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t'
            
                                    tmpcounter += 1
                                line_print += '\n'
                                line_print += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                                tree = str(tmptree[4])
            line_print += '\n' + '*' * 120 + '\n'

            #line_print += fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump, pid_procdump
            for line_vol_yara in data_vol_yara:
                ownername_vol_yara, pid_vol_yara, rule_vol_yara, data_offset_vol_yara,\
                data_bytes_vol_yara, data_txt_vol_yara = line_vol_yara
                if str(pid_vol_yara) == str(pid_procdump):
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - ProcDump vs volatility_Yara' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + fullfilename_procdump + '\n'
                    line_print += 'PE Compile time     : ' + name_procdump + '\n'
                    line_print += 'Filename Procdmp    : ' + filename_procdump + '\n'
                    line_print += 'Pid from Procdump   : ' + pid_procdump + '\n'
                    line_print += 'Pid from yara       : ' + str(pid_vol_yara) + '\n'
                    line_print += 'Ownername Yara      : ' + ownername_vol_yara + '\n' + '\n'
                    data_offset_vol_yara = data_offset_vol_yara.split('\n')
                    data_bytes_vol_yara = data_bytes_vol_yara.split('\n')
                    data_txt_vol_yara = data_txt_vol_yara.split('\n')
                    linenr = 0
                    line_print += '=' * 88 + '\nYaradata\n' + '=' * 88
                    for test in data_offset_vol_yara:
                        line_print += '\n' + data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr]
                        linenr += 1
                    line_print += '\n' + '=' * 88 + '\n'

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_procdump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Procdump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_procdump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Procdump vs PE_Scan' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe + '\n'
                    line_print += 'PE Compile time     : ' + Pe_Compiletime + '\n'
                    line_print += 'PE Packer           : ' + Pe_Packer + '\n'
                    line_print += 'File type PE file   : ' + Filetype_pe + '\n'
                    line_print += 'Original Filename   : ' + Original_Filename_pe + '\n'
                    line_print += 'Yara Result         : ' + Yara_Results_pe + '\n' + '\n'

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_procdump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Procdump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:       ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info:            \n' + Pe_Blob_beta + '\n\n'

        if item[0] == 'moddump':
            a, fullfilename_moddump, name_moddump, filename_moddump, md5hash_moddump, modulename_moddump = item
            pid_moddump = filename_moddump.split('.')[1]
            line_print += '\n***********************************' + '\n'
            line_print += 'collecting info for file : ' + fullfilename_moddump + '\n'
            line_print += 'Name from moddump        : ' + name_moddump + '\n'
            line_print += 'Filename from moddump    : ' + filename_moddump + '\n'
            line_print += 'Module from moddump      : ' + modulename_moddump + '\n'
            line_print += 'MD5 Hash from moddump    : ' + md5hash_moddump + '\n'
            #line_print += 'Pid from moddump         : ' + pid_moddump + '\n' # Moddump heeft geen PID
            line_print += '***********************************\n\n'

            for line_psxview in data_psxview:
                offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
                pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
                if str(pid_psxview) == str(pid_moddump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Match - Pid from PSXview vs Moddump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
                    tmpcounter = 0
                    for tmplen in line_psxview:
                        if len(str(tmp[tmpcounter])) < len(str(line_psxview[tmpcounter])):
                            line_print += tmp[tmpcounter] + '\t\t'
                        else:
                            line_print += tmp[tmpcounter] + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    for tmplen in line_psxview:
                        line_print += str(line_psxview[tmpcounter]) + \
                                      ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                        tmpcounter += 1
                    line_print += '\n'

            list_pstree = []
            for line_pstree in data_pstree:
                depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
                plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
                list_pstree.append(line_pstree)
                if str(pid_pstree) == str(pid_moddump):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Build pidtree - Pid from PSTree vs Moddump'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
                    tmpcounter = 0
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if tmpcounter >= 2:
                            line_print += str(tmp[tmpcounter]) + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += line_pstree[tmpcounter + 1] + '\t'
                        if tmpcounter >= 2:
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t'

                        tmpcounter += 1
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
                    tree = str(line_pstree[4])
                    while tree != '0':
                        tmpcounter = 0
                        for tmptree in list_pstree:
                            #line_print += str(tmptree[4]) + '\t' + str(line_pstree[3]) + '\n'
                            # pid  = 3
                            # ppid = 4
                            #if str(tmptree[4]) != '0':
                            if str(tmptree[3]) == tree:
                                line_print += '\n' + '-' * 120 + '\n'
                                line_print += '-' * int(tmptree[0]) + ' '
                                for tmplen in tmp:
                                    if str(tmp[tmpcounter]) == 'offset':
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t\t'
                                    if str(tmp[tmpcounter]) == 'name':
                                        line_print += tmptree[tmpcounter + 1] + '\t'
                                        if tmptree[tmpcounter + 1] == 'System':
                                            line_print += '\t'

                                    if tmpcounter >= 2:
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t'

                                    tmpcounter += 1
                                line_print += '\n'
                                line_print += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                                tree = str(tmptree[4])
            line_print += '\n' + '*' * 120 + '\n'

            for line_vol_yara in data_vol_yara:
                ownername_vol_yara, pid_vol_yara, rule_vol_yara, data_offset_vol_yara,\
                data_bytes_vol_yara, data_txt_vol_yara = line_vol_yara
                if str(pid_vol_yara) == str(pid_moddump):
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Moddump vs volatility_Yara' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + fullfilename_moddump + '\n'
                    line_print += 'PE Compile time     : ' + name_moddump + '\n'
                    line_print += 'Filename moddmp     : ' + filename_moddump + '\n'
                    line_print += 'Pid from moddump    : ' + pid_moddump + '\n'
                    line_print += 'Pid from yara       : ' + pid_vol_yara + '\n'
                    line_print += 'Ownername Yara      : ' + name_vol_yara + '\n'
                    line_print += 'Ownername Yara      : ' + rule_vol_yara + '\n'
                    data_offset_vol_yara = data_offset_vol_yara.split('\n')
                    data_bytes_vol_yara = data_bytes_vol_yara.split('\n')
                    data_txt_vol_yara = data_txt_vol_yara.split('\n')
                    linenr = 0
                    line_print += '=' * 88 + '\nYaradata\n' + '=' * 88
                    for test in data_offset_vol_yara:
                        line_print += '\n' + data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr]
                        linenr += 1
                    line_print += '\n' + '=' * 88 + '\n'

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_moddump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Moddump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_moddump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Moddump vs PE_Scan' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe + '\n'
                    line_print += 'PE Compile time     : ' + Pe_Compiletime + '\n'
                    line_print += 'PE Packer           : ' + Pe_Packer + '\n'
                    line_print += 'File type PE file   : ' + Filetype_pe + '\n'
                    line_print += 'Original Filename   : ' + Original_Filename_pe + '\n'
                    line_print += 'Yara Result         : ' + Yara_Results_pe + '\n\n'

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_moddump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - moddump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n\n'

        # Collect data where photorec is the source (md5).

        if item[0] == 'photorec':
            a, fullfilename_photorec, md5hash_photorec = item
            #line_print += fullfilename_photorec, md5hash_photorec
            for line_yara in data_yara:
                filename_yara, string_yara, yara_yara, yara_description_yara = line_yara
                if filename_yara == fullfilename_photorec:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Photorec vs volatility_Yara' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + fullfilename_photorec + '\n'
                    line_print += 'MD5 Hash            : ' + md5hash_photorec + '\n'
                    line_print += 'Filename Yara       : ' + filename_yara + '\n'
                    line_print += 'Yara string         : ' + string_yara + '\n'
                    line_print += 'yara                : ' + yara_yara + '\n'
                    line_print += 'Yara description    : ' + yara_description_yara + '\n\n'

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_photorec:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Photorec vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_photorec:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Photorec vs PE_Scan' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe + '\n'
                    line_print += 'PE Compile time     : ' + Pe_Compiletime + '\n'
                    line_print += 'PE Packer           : ' + Pe_Packer + '\n'
                    line_print += 'File type PE file   : ' + Filetype_pe + '\n'
                    line_print += 'Original Filename   : ' + Original_Filename_pe + '\n'
                    line_print += 'Yara Result         : ' + Yara_Results_pe + '\n\n'

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_photorec:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Photorec vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n\n'

    lprint += line_print
    print line_print
    sprint += line_print
    line_print = ''

#########################################################################################
#########################################################################################
#
#   ClamAV Scan
#########################################################################################
#########################################################################################
    cprint += '\n***********************************' + '\n'
    cprint += 'ClamAV findings'
    cprint += '\n***********************************' + '\n'
    for line_pe_scan_beta in data_pe_scan_beta:
        pe_scan_beta_filename, pe_scan_beta_pe_blob = line_pe_scan_beta
        tmp_pe_scan_beta_pe_blob = pe_scan_beta_pe_blob.split('\n')
        for test_clam in tmp_pe_scan_beta_pe_blob:
            if 'Clamav' in test_clam:
                clam_line = test_clam.split(':')
                if clam_line[0] == 'Clamav' and clam_line[2].strip(' ') != 'OK':
                    for item in clam_line:
                        cprint += item + '\t'
                    cprint += '\n'
                    cprint += pe_scan_beta_pe_blob + '\n'

#########################################################################################
#########################################################################################
# Done
#########################################################################################
#   Find unlinked dll's with ldrmodules. (inload, Ininit, Inmem = false)
#   - alert if ininit is false and mappedpath is empty!
#   SELECT * FROM `ldrmodules_v` WHERE mappedpath = '' AND ininit = 'False';
#########################################################################################
#########################################################################################

    data_ldrmod = Lobotomy.get_databasedata('pid,process,base,inload,ininit,inmem,mappedpath,loadpathpath,'
                                            'loadpathprocess, initpathpath, initpathprocess, mempathpath,'
                                            'mempathprocess', 'ldrmodules_v', database)

    for line_ldrmodules in data_ldrmod:
        ldr_pid, ldr_process, ldr_base, ldr_inload, ldr_ininit, ldr_inmem, ldr_mappedpath, ldr_loadpathpath, \
        ldr_loadpathprocess, ldr_initpathpath, ldr_initpathprocess, ldr_mempathpath, ldr_mempathprocess = line_ldrmodules

        if ldr_mappedpath == '' and ldr_ininit == 'False':
            line_print += '\n***********************************' + '\n'
            line_print += 'Possible unlinked Dll found' + '\n'
            line_print += 'Empty Ldr_Mappedpath and Ldr_ininit is False: Alert' + '\n'
            line_print += '***********************************' + '\n'
            line_print += 'Process         : ' + ldr_process + '\n'
            line_print += 'Mapped Path     : ' + ldr_mappedpath + '\n'
            line_print += 'Base            : ' + ldr_base + '\n'
            line_print += 'Pid Ldrmodules  : ' + str(ldr_pid) + '\n'
            line_print += 'Inload          : ' + ldr_inload + '\n'
            line_print += 'Inload process  : ' + ldr_loadpathprocess + '\n'
            line_print += 'Inload path     : ' + ldr_loadpathpath + '\n'
            line_print += 'Ininint         : ' + ldr_ininit + '\n'
            line_print += 'Ininint process : ' + ldr_initpathprocess + '\n'
            line_print += 'Ininint path    : ' + ldr_initpathpath + '\n'
            line_print += 'Inmem           : ' + ldr_inmem + '\n'
            line_print += 'Inmem process   : ' + ldr_mempathprocess + '\n'
            line_print += 'Inmem path      : ' + ldr_mempathpath + '\n\n'

            for line_psxview in data_psxview:
                offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
                pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
                if str(pid_psxview) == str(ldr_pid):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Match - Pid from PSXview vs Ldrmodules'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
                    tmpcounter = 0
                    for tmplen in line_psxview:
                        if len(str(tmp[tmpcounter])) <= 8 and len(str(line_psxview[tmpcounter])) <= 8:# or len(str(tmp[tmpcounter])) <= len(str(line_psxview[tmpcounter])):
                            line_print += tmp[tmpcounter] + '\t'
                        else:
                            line_print += tmp[tmpcounter] + '\t\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    for tmplen in line_psxview:
                        line_print += str(line_psxview[tmpcounter]) + \
                                      ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                        tmpcounter += 1
                    line_print += '\n'

            list_pstree = []
            for line_pstree in data_pstree:
                depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
                plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
                list_pstree.append(line_pstree)
                if str(pid_pstree) == str(ldr_pid):
                    line_print += '\n' + '*' * 120 + '\n'
                    line_print += 'Build pidtree - Pid from PSTree vs Ldrmodues'
                    line_print += '\n' + '*' * 120 + '\n'
                    tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
                    tmpcounter = 0
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += tmp[tmpcounter] + '\t\t'
                        if tmpcounter >= 2:
                            line_print += str(tmp[tmpcounter]) + '\t'
                        tmpcounter += 1
                    tmpcounter = 0
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' '
                    for tmplen in tmp:
                        if str(tmp[tmpcounter]) == 'offset':
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t\t'
                        if str(tmp[tmpcounter]) == 'name':
                            line_print += line_pstree[tmpcounter + 1] + '\t'
                        if tmpcounter >= 2:
                            line_print += str(line_pstree[tmpcounter + 1]) + '\t'

                        tmpcounter += 1
                    line_print += '\n'
                    line_print += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
                    line_print += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
                    tree = str(line_pstree[4])
                    while tree != '0':
                        tmpcounter = 0
                        for tmptree in list_pstree:
                            #line_print += str(tmptree[4]) + '\t' + str(line_pstree[3]) + '\n'
                            # pid  = 3
                            # ppid = 4
                            #if str(tmptree[4]) != '0':
                            if str(tmptree[3]) == tree:
                                line_print += '\n' + '-' * 120 + '\n'
                                line_print += '-' * int(tmptree[0]) + ' '
                                for tmplen in tmp:
                                    if str(tmp[tmpcounter]) == 'offset':
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t\t'
                                    if str(tmp[tmpcounter]) == 'name':
                                        line_print += tmptree[tmpcounter + 1] + '\t'
                                        if tmptree[tmpcounter + 1] == 'System':
                                            line_print += '\t'
                                    if tmpcounter >= 2:
                                        line_print += str(tmptree[tmpcounter + 1]) + '\t'

                                    tmpcounter += 1
                                line_print += '\n'
                                line_print += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                                line_print += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                                tree = str(tmptree[4])
                    line_print += '\n' + '*' * 120 + '\n'

#########################################################################################
#########################################################################################
#   Add Malfind plugin to ldrinfo
#########################################################################################
#########################################################################################

            for line_malfind in data_malfind:
                process_malfind, pid_malfind, address_malfind, vadtag_malfind, protection_malfind, \
                flags_malfind, header_malfind, body_malfind = line_malfind
                if str(pid_malfind) == str(ldr_pid) and int(address_malfind, 0) == int(ldr_base, 0):
                    print '\nProcess: ' + process_malfind + '\tPid: ' + str(pid_malfind) + '\tAddress: ' + address_malfind
                    print '\nVad: ' + vadtag_malfind + '\tProtection: ' + protection_malfind
                    print flags_malfind
                    print header_malfind
                    print body_malfind
                    line_print += '\nProcess: ' + process_malfind
                    line_print += '\tPid: ' + str(pid_malfind)
                    line_print += '\tAddress: ' + address_malfind
                    line_print += '\nVad: ' + vadtag_malfind
                    line_print += '\tProtection: ' + protection_malfind
                    line_print += '\n' + flags_malfind
                    line_print += '\n' + header_malfind
                    line_print += '\n' + body_malfind




        if ldr_loadpathpath != ldr_initpathpath or ldr_loadpathpath != ldr_mempathpath or ldr_mempathpath != ldr_initpathpath:
            if ldr_ininit == 'True' and ldr_inload == 'True' and ldr_inmem == 'True':
                line_print += '\n***********************************' + '\n'
                line_print += 'Non matching Paths + inmem, ininit and inload while Inload + Inmem and Ininit are True: Alert' + '\n'
                line_print += '***********************************' + '\n'
                line_print += 'Process         : ' + ldr_process + '\n'
                line_print += 'Mapped Path     : ' + ldr_mappedpath + '\n'
                line_print += 'Base            : ' + ldr_base + '\n'
                line_print += 'Pid Ldrmodules  : ' + str(ldr_pid) + '\n'
                line_print += 'Inload          : ' + ldr_inload + '\n'
                line_print += 'Inload process  : ' + ldr_loadpathprocess + '\n'
                line_print += 'Inload path     : ' + ldr_loadpathpath + '\n'
                line_print += 'Ininint         : ' + ldr_ininit + '\n'
                line_print += 'Ininint process : ' + ldr_initpathprocess + '\n'
                line_print += 'Ininint path    : ' + ldr_initpathpath + '\n'
                line_print += 'Inmem           : ' + ldr_inmem + '\n'
                line_print += 'Inmem process   : ' + ldr_mempathprocess + '\n'
                line_print += 'Inmem path      : ' + ldr_mempathpath + '\n\n'
                for line_psxview in data_psxview:
                    offset_psxview, name_psxview, pid_psxview, pslist_psxview, psscan_psxview, thrdproc_psxview, \
                    pspcid_psxview, csrss_psxview, session_psxview, deskthrd_psxview, exittime_psxview = line_psxview
                    if str(pid_psxview) == str(ldr_pid):
                        line_print += '\n' + '*' * 120 + '\n'
                        line_print += 'Match - Pid from PSXview vs Ldrmodules'
                        line_print += '\n' + '*' * 120 + '\n'
                        tmp = ['offset','name','pid','pslist','psscan','thrdproc','pspcid','csrss','session','deskthrd','exittime']
                        tmpcounter = 0
                        for tmplen in line_psxview:
                            if len(str(tmp[tmpcounter])) <= 8 and len(str(line_psxview[tmpcounter])) <= 8:# or len(str(tmp[tmpcounter])) <= len(str(line_psxview[tmpcounter])):
                                line_print += tmp[tmpcounter] + '\t'
                            else:
                                line_print += tmp[tmpcounter] + '\t\t'
                            tmpcounter += 1
                        tmpcounter = 0
                        line_print += '\n'
                        for tmplen in line_psxview:
                            line_print += str(line_psxview[tmpcounter]) + \
                                          ' ' * (len(str(tmp[tmpcounter])) - len(str(line_psxview[tmpcounter]))) + '\t'
                            tmpcounter += 1
                        line_print += '\n'

                list_pstree = []
                for line_pstree in data_pstree:
                    depth_pstree, offset_pstree, name_pstree, pid_pstree, ppid_pstree, thds_pstree, hnds_pstree, \
                    plugin_time_pstree, audit_pstree, cmd_pstree, path_pstree = line_pstree
                    list_pstree.append(line_pstree)
                    print pid_pstree, ldr_pid
                    if str(pid_pstree) == str(ldr_pid):
                        line_print += '\n' + '*' * 120 + '\n'
                        line_print += 'Build pidtree - Pid from PSTree vs Ldrmodules'
                        line_print += '\n' + '*' * 120 + '\n'
                        tmp = ['offset', 'name', 'pid', 'ppid', 'thds', 'hnds', 'plugin_time']
                        tmpcounter = 0
                        line_print += '-' * int(depth_pstree) + ' '
                        for tmplen in tmp:
                            if str(tmp[tmpcounter]) == 'offset':
                                line_print += tmp[tmpcounter] + '\t\t'
                            if str(tmp[tmpcounter]) == 'name':
                                line_print += tmp[tmpcounter] + '\t\t'
                            if tmpcounter >= 2:
                                line_print += str(tmp[tmpcounter]) + '\t'
                            tmpcounter += 1
                        tmpcounter = 0
                        line_print += '\n'
                        line_print += '-' * int(depth_pstree) + ' '
                        for tmplen in tmp:
                            if str(tmp[tmpcounter]) == 'offset':
                                line_print += str(line_pstree[tmpcounter + 1]) + '\t\t'
                            if str(tmp[tmpcounter]) == 'name':
                                line_print += line_pstree[tmpcounter + 1] + '\t'
                            if tmpcounter >= 2:
                                line_print += str(line_pstree[tmpcounter + 1]) + '\t'

                            tmpcounter += 1
                        line_print += '\n'
                        line_print += '-' * int(depth_pstree) + ' Audit : ' + audit_pstree + '\n'
                        line_print += '-' * int(depth_pstree) + ' Cmd   : ' + cmd_pstree + '\n'
                        line_print += '-' * int(depth_pstree) + ' Path  : ' + path_pstree
                        tree = str(line_pstree[4])
                        # counter = 0
                        while tree != '0':
                        #     counter += 1
                        #     if counter == 500:
                        #         tree = 0
                            tmpcounter = 0
                            for tmptree in list_pstree:
                                #line_print += str(tmptree[4]) + '\t' + str(line_pstree[3]) + '\n'
                                # pid  = 3
                                # ppid = 4
                                #if str(tmptree[4]) != '0':
                                if str(tmptree[3]) == tree:
                                    line_print += '\n' + '-' * 120 + '\n'
                                    line_print += '-' * int(tmptree[0]) + ' '
                                    for tmplen in tmp:
                                        if str(tmp[tmpcounter]) == 'offset':
                                            line_print += str(tmptree[tmpcounter + 1]) + '\t\t'
                                        if str(tmp[tmpcounter]) == 'name':
                                            line_print += tmptree[tmpcounter + 1] + '\t'
                                            if tmptree[tmpcounter + 1] == 'System':
                                                line_print += '\t'
                                        if tmpcounter >= 2:
                                            line_print += str(tmptree[tmpcounter + 1]) + '\t'

                                        tmpcounter += 1
                                    line_print += '\n'
                                    line_print += '-' * int(tmptree[0]) + ' Audit : ' + tmptree[8] + '\n'
                                    line_print += '-' * int(tmptree[0]) + ' Cmd   : ' + tmptree[9] + '\n'
                                    line_print += '-' * int(tmptree[0]) + ' Path  : ' + tmptree[10]
                                    tree = str(tmptree[4])
                        line_print += '\n' + '*' * 120 + '\n'

#########################################################################################
#########################################################################################
#   Add Malfind plugin to ldrinfo
#########################################################################################
#########################################################################################

                for line_malfind in data_malfind:
                    process_malfind, pid_malfind, address_malfind, vadtag_malfind, protection_malfind, \
                    flags_malfind, header_malfind, body_malfind = line_malfind
                    if str(pid_malfind) == str(ldr_pid) and int(address_malfind, 0) == int(ldr_base, 0):
                        print '\nProcess: ' + process_malfind + '\tPid: ' + str(pid_malfind) + '\tAddress: ' + address_malfind
                        print '\nVad: ' + vadtag_malfind + '\tProtection: ' + protection_malfind
                        print flags_malfind
                        print header_malfind
                        print body_malfind
                        line_print += '\nProcess: ' + process_malfind
                        line_print += '\tPid: ' + str(pid_malfind)
                        line_print += '\tAddress: ' + address_malfind
                        line_print += '\nVad: ' + vadtag_malfind
                        line_print += '\tProtection: ' + protection_malfind
                        line_print += '\n' + flags_malfind
                        line_print += '\n' + header_malfind
                        line_print += '\n' + body_malfind


#########################################################################################
#########################################################################################
# Malicious Callbacks
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

    callbacktype_from_file = []
    callbackmodule_from_file = []
    timersmodule_from_file = []
    call_timer = []
    data_callbacks = Lobotomy.get_databasedata('type,callback,module,details', 'callbacks', database)
    data_timers = Lobotomy.get_databasedata('offset,duetime,period,signaled,routine,module', 'timers', database)
    data_driverscan = Lobotomy.get_databasedata('offset,ptr,hnd,start,size,servicekey,name,drivername', 'driverscan', database)

    # with open('lobotomy_threatlist.txt') as f:
    #     for line in f:

    for line in lobotomy_threatlist:
        if not line.startswith('#'):
            if line.startswith('callbacks:type'):
                callbacktype_from_file.append(line.strip('\n').split(':')[2])
            if line.startswith('callbacks:module'):
                callbackmodule_from_file.append(line.strip('\n').split(':')[2])
            if line.startswith('timers:module'):
                timersmodule_from_file.append(line.strip('\n').split(':')[2])

    cprint += '\n' + '*' * 120 + '\n'
    cprint += 'Searching for: Malicious Callbacks'
    cprint += '\n' + '*' * 120 + '\n'

    alertcallbackmodule = 0
    alertcallbackmodulefile = 0
    alertcallbacktypefile = 0
    for line_callbacks in data_callbacks:
        type_callbacks, callback_callbacks, module_callbacks, details_callbacks = line_callbacks
        if module_callbacks == 'UNKNOWN':
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if alertcallbackmodule == 0:
                print '\n' + '*' * 120 + '\n'
                print 'Alert: Unknown Module in Callback:'
                cprint += '\n' + '*' * 120 + '\n'
                cprint += 'Alert: Unknown Module in Callback: \n'
                alertcallbackmodule = 1
            print line_callbacks
            cprint += str(line_callbacks) + '\n'
            tmp = module_callbacks, line_callbacks
            call_timer.append(tmp)
            module_callbacks = ''

        for callback_alert in callbacktype_from_file:
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if type_callbacks == callback_alert:
                if alertcallbacktypefile == 0:
                    print '\n' + '*' * 120 + '\n'
                    print "Alert: Callback 'Type' from Lobotomy Threatlist: \n"
                    cprint += '\n' + '*' * 120 + '\n'
                    cprint += "Alert: Callback 'Type' from Lobotomy Threatlist: \n"
                    alertcallbacktypefile = 1
                print line_callbacks
                cprint += str(line_callbacks) + ' \n'
                tmp = module_callbacks, line_callbacks
                call_timer.append(tmp)

        for callback_alert in callbackmodule_from_file:
            # Collect info and display them later. otherwise there will be a print line between event alert.
            if module_callbacks == callback_alert:
                if alertcallbackmodulefile == 0:
                    print '\n' + '*' * 120 + '\n'
                    print "Alert: Callback 'Module' from Lobotomy Threatlist: \n"
                    cprint += '\n' + '*' * 120 + '\n'
                    cprint += "Alert: Callback 'Module' from Lobotomy Threatlist: \n"
                    alertcallbackmodulefile = 1
                print line_callbacks
                cprint += str(line_callbacks) + ' \n'
                tmp = module_callbacks, line_callbacks
                call_timer.append(tmp)

    cprint += '\n' + '*' * 120 + '\n'
    cprint += 'Searching for: Malicious Timers'
    cprint += '\n' + '*' * 120 + '\n'

    alerttimercallback = 0
    for line_timers in data_timers:
        offset_timers, duetime_timers, period_timers, signaled_timers, routine_timers, module_timers = line_timers
        if module_timers == 'UNKNOWN':
            print '\n' + '*' * 120 + '\n'
            print 'Alert: Unknown Module in Timers: \n', line_timers
            cprint += '\n' + '*' * 120 + '\n'
            cprint += 'Alert: Unknown Module in Timers:\n' + str(line_timers)
            for tmp_callbacks in call_timer:
                for item in tmp_callbacks:
                    if item == module_timers:
                        if alerttimercallback == 0:
                            print '\n' + '*' * 120 + '\n'
                            print 'Alert: Match between timers en callbacks\n'
                            cprint += '\n' + '*' * 120 + '\n'
                            cprint += 'Alert: Match between timers en callbacks'
                            alerttimercallback = 1
                        print 'Callbacks: ' + str(tmp_callbacks[1]) + '\n' + 'Timers   : ' + str(line_timers)
                        cprint += 'Callbacks: ' + str(tmp_callbacks[1]) + '\n' + 'Timers   : ' + str(line_timers)

                        for line_driverscan in data_driverscan:
                            offset_driverscan, ptr_driverscan, hnd_driverscan, start_driverscan, size_driverscan, \
                                servicekey_driverscan, name_driverscan, drivername_driverscan = line_driverscan
                            if str(tmp_callbacks[1][3]) == str(name_driverscan):   # callbacks.details matches driverscan.drivername
                                print '\nWe might have a match between the name from Plugin Callbacks and Driverscan:' \
                                      '\nDrivername: ' + str(drivername_driverscan)
                                print 'Plugin Driverscan: ' + str(line_driverscan)
                                print 'Plugin Callbacks : ' + str(tmp_callbacks)
                                cprint += '\nWe might have a match between the name from Plugin Callbacks and ' \
                                          'Driverscan:\nDrivername:' + str(drivername_driverscan) + '\n'
                                cprint += 'Plugin Driverscan: ' + str(line_driverscan) + '\n'
                                cprint += 'Plugin Callbacks : ' + str(tmp_callbacks) + '\n'

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


# todo

                # OrphanThread = 'Detect orphan threads',
                # SystemThread = 'Detect system threads',
                # HookedSSDT = 'Detect threads using a hooked SSDT',
                # ScannerOnly = 'Detect threads no longer in a linked list',
                # DkomExit = 'Detect inconsistencies wrt exit times and termination',
                # HideFromDebug = 'Detect threads hidden from debuggers',
                # HwBreakpoints = 'Detect threads with hardware breakpoints',
                # AttachedProcess = 'Detect threads attached to another process',


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


    print '\n\n#########################################################################################'
    print '#########################################################################################'
    print '# Dumping Suspicious Processes'
    print '#########################################################################################'

    #data_psscan = Lobotomy.get_databasedata('offset,name,pid,ppid,pdb,timecreated,timeexited', 'psscan', database)
    data_pslist = Lobotomy.get_databasedata('offset,name,pid,ppid,thds,hnds,sess,wow64', 'pslist', database)
    tmp = ''
    tmpcounter = 0
    a = ''
    for line_pslist in data_pslist:
        # Add all processes from pslist in a string
        tmp += str(line_pslist[1]) + ' '

    for line_psxview in data_psxview:
        # test if process from psxview does not match data from pslist and if exittime doesn't have a value
        if line_psxview[1] not in tmp and line_psxview[10] == None:
            print 'error', line_psxview


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



#########################################################################################
#########################################################################################
# SSDT Inline Hooking
#########################################################################################

    # id	ssdt	mem1	entry	mem2	systemcall	owner	hookaddress	hookprocess
    # 977	SSDT[0]	80501b8c	0x0019	0xb240f80e	NtClose	PROCMON20.SYS

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
                print 'alert: ssdt 0 hook'
            if line_ssdt[0] == 'ssdt[1]' and \
                line_ssdt[5] != 'win32k.sys':
                print 'alert: ssdt 1 hook'
                pass
            if line_ssdt[6] != '':
                print 'Alert      : ssdt hook\nHookadress : {}\nHookProcess: {}'.format(line_ssdt[6], line_ssdt[7])

                print line_ssdt
                print 'next step: dumping hooked process'


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





    try:
        lprint += line_print
    except:
        pass
    try:
        sprint += line_print
    except:
        pass
    try:
        sprint += cprint
    except:
        pass
    line_print = ''
    #print sprint
    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(sprint)
        f.close()
    except:
        pass

    # lobotomy_report
    if DEBUG:
        print SQL_cmd
    else:
        sprint = sprint.replace("'", '"')
        SQL_cmd = "INSERT INTO lobotomy_report VALUES (0, '{}')".format(sprint)
        Lobotomy.exec_sql_query(SQL_cmd, database)
        Lobotomy.plugin_stop('lobotomy_report', database)
        Lobotomy.plugin_pct('lobotomy_report', database, 100)






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


    print line_print

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <database>"
    else:
        main(sys.argv[1])
