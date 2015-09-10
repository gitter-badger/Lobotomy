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
    #Lobotomy.plugin_start(plugin, database)
    #Lobotomy.plugin_pct(plugin, database, 1)
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

            print 'Running pstree for Dlldump'
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

            print 'Running pstree for Procdump'
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

            print 'Running pstree for Moddump'
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

        if ldr_loadpathpath != ldr_initpathpath or ldr_loadpathpath != ldr_mempathpath or ldr_mempathpath != ldr_initpathpath:
            if ldr_ininit == 'True' and ldr_inload == 'True' and ldr_inmem == 'True':
                line_print += '\n***********************************' + '\n'
                line_print += 'Non matching Paths + inmem + ininit and inload while Inload + Inmem and Ininit are True: Alert' + '\n'
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
    data_callbacks = Lobotomy.get_databasedata('type,callback,module,details', 'callbacks', database)

    # with open('lobotomy_threatlist.txt') as f:
    #     for line in f:

    for line in lobotomy_threatlist:
        if not line.startswith('#'):
            if line.startswith('callbacks:type'):
                callbacktype_from_file.append(line.strip('\n').split(':')[2])
            if line.startswith('callbacks:module'):
                callbackmodule_from_file.append(line.strip('\n').split(':')[2])

    cprint += '\n' + '*' * 120 + '\n'
    cprint += 'Searching for: Malicious Callbacks'
    cprint += '\n' + '*' * 120 + '\n'

    for line_callbacks in data_callbacks:
        type_callbacks, callback_callbacks, module_callbacks, details_callbacks = line_callbacks
        if module_callbacks == 'UNKNOWN':
            print 'Alert: Unknown Module in Callback: \n ', line_callbacks
            cprint += 'Alert: Unknown Module in Callback: \n ' + str(line_callbacks)
        for callback_alert in callbacktype_from_file:
            if type_callbacks == callback_alert:
                print "Alert: Callback 'Type' from Lobotomy Threatlist: \n", line_callbacks
                cprint += "Alert: Callback 'Type' from Lobotomy Threatlist: \n" + str(line_callbacks) + ' \n'
        for callback_alert in callbackmodule_from_file:
            if module_callbacks == callback_alert:
                print "Alert: Callback 'Module' from Lobotomy Threatlist: \n", line_callbacks
                cprint += "Alert: Callback 'Module' from Lobotomy Threatlist: \n" + str(line_callbacks) + ' \n'


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
