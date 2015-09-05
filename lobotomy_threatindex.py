# coding=utf-8
__author__ = 'Wim Venhuizen'

#
# Script version    0.5
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

import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()
plugin = "threatscanner"

DEBUG = False


def main(database):
    #Lobotomy.plugin_start(plugin, database)
    #Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]

    # Read database

    starttime = time.time()
    sprint = ''
    cprint = ''
    lprintstart = ''
    lprintstart = 'Reading Database, please wait\n'
    lprintstart += 'start-time: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n'
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

    bad_hashes_list = []
    stoptime = time.time()
    lprintstart += 'seconds to read database(s)' +str(round(stoptime - starttime)) + '\n'
    starttime = time.time()
    lprintstart += 'start-time: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n'
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
    sprint += lprintdlldump

    lprintprocdump = ''
    for line_procdump in data_procdump:
        fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = line_procdump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_procdump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_procdump:
                    lprintprocdump += '\n***********************************' + '\n'
                    lprintprocdump += 'Match - Volatility plugin: Moddump. ' + '\n'
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
            #line_print += fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump, pid_dlldump
            # data_vol_yara = Lobotomy.get_databasedata('owner_name,pid,rule,name,data_offset,data_bytes,data_txt',
            #                               'volatility_yarascan', database)

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
                    for test in data_offset_vol_yara:
                        line_print += data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr] + '\n'
                        linenr += 1

                    # line_print += '\n\n\n***********************************\nmatch DLLDump vs volatility_Yara \n***********************************'
                    # line_print += fullfilename_dlldump, modulename_dlldump, filename_dlldump, pid_dlldump
                    # line_print += ownername_vol_yara, pid_vol_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_dlldump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - DLLDump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n'
                    # line_print += '\n***********************************\nmatch DLLDump vs Exifinfo \n***********************************'
                    # line_print += "Exifinfo filename \t\t:", filename_exifinfo
                    # line_print += exifinfo

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
                    # line_print += '\n***********************************\nmatch DLLDump vs PE_Scan \n***********************************'
                    # line_print += Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_dlldump:
                    line_print += 'Match - DLLDump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n' + '\n'
                    # line_print += '\n***********************************\nmatch DLLDump vs PE_Scan_beta \n***********************************'
                    # line_print += '\n***********************************'
                    # line_print += Fullfilename_pe_beta, Pe_Blob_beta


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
                    for test in data_offset_vol_yara:
                        line_print += data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr] + '\n'
                        linenr += 1
                    #
                    # line_print += '\n\n\n***********************************\nmatch ProcDump vs volatility_Yara \n***********************************'
                    # line_print += fullfilename_procdump, name_procdump, filename_procdump, pid_procdump
                    # line_print += ownername_vol_yara, pid_vol_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_procdump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Procdump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'
                    # line_print += '\n***********************************\nmatch ProcDump vs Exifinfo \n***********************************'
                    # line_print += "Exifinfo filename \t\t:", filename_exifinfo
                    # line_print += exifinfo

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
                    # line_print += '\n***********************************\nmatch ProcDump vs PE_Scan \n***********************************'
                    # line_print += Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_procdump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Procdump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:       ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info:            \n' + Pe_Blob_beta + '\n\n'
                    # line_print += '\n***********************************\nmatch ProcDump vs PE_Scan_beta \n***********************************'
                    # line_print += Fullfilename_pe_beta, Pe_Blob_beta

        if item[0] == 'moddump':
            a, fullfilename_moddump, name_moddump, filename_moddump, md5hash_moddump, modulename_moddump = item
            pid_moddump = filename_moddump.split('.')[1]
            line_print += '\n***********************************' + '\n'
            line_print += 'collecting info for file : ' + fullfilename_moddump + '\n'
            line_print += 'Name from moddump        : ' + name_moddump + '\n'
            line_print += 'Filename from moddump    : ' + filename_moddump + '\n'
            line_print += 'Module from moddump      : ' + modulename_moddump + '\n'
            line_print += 'MD5 Hash from moddump    : ' + md5hash_moddump + '\n'
            line_print += 'Pid from moddump         : ' + pid_moddump + '\n'
            line_print += '***********************************\n\n'

            #line_print += fullfilename_moddump, name_moddump, filename_moddump, md5hash_moddump, pid_moddump
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
                    for test in data_offset_vol_yara:
                        line_print += data_offset_vol_yara[linenr] + '\t' + data_bytes_vol_yara[linenr] + '\t' + \
                                      data_txt_vol_yara[linenr] + '\n'
                        linenr += 1
                    #
                    # line_print += '\n\n\n***********************************\nmatch modDump vs volatility_Yara \n***********************************'
                    # line_print += fullfilename_moddump, name_moddump, filename_moddump, pid_moddump
                    # line_print += ownername_vol_yara, pid_vol_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_moddump:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Moddump vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'
                    # line_print += '\n***********************************\nmatch modDump vs Exifinfo \n***********************************'
                    # line_print += "Exifinfo filename \t\t:", filename_exifinfo
                    # line_print += exifinfo

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
                    # line_print += '\n***********************************\nmatch modDump vs PE_Scan \n***********************************'
                    # line_print += Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_moddump:
                    line_print += 'Match - moddump vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n\n'
                    # line_print += '\n***********************************\nmatch modDump vs PE_Scan_beta \n***********************************'
                    # line_print += Fullfilename_pe_beta, Pe_Blob_beta

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
                    # line_print += '\n\n\n***********************************\nmatch Photorec vs Yara \n***********************************'
                    # line_print += fullfilename_photorec, md5hash_photorec
                    # line_print += filename_yara, string_yara, yara_yara, yara_description_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_photorec:
                    line_print += '\n***********************************' + '\n'
                    line_print += 'Match - Photorec vs Exifinfo' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename:                  ' + filename_exifinfo + '\n'
                    line_print += exifinfo + '\n\n'
                    # line_print += '\n***********************************\nmatch Photorec vs Exifinfo \n***********************************'
                    # line_print += "Exifinfo filename \t\t:", filename_exifinfo
                    # line_print += exifinfo

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
                    # line_print += '\n***********************************\nmatch Photorec vs PE_Scan \n***********************************'
                    # line_print += Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_photorec:
                    line_print += 'Match - Photorec vs PE_Scan_Beta' + '\n'
                    line_print += '***********************************' + '\n'
                    line_print += 'Fullfilename        : ' + Fullfilename_pe_beta + '\n'
                    line_print += 'PE info             :\n' + Pe_Blob_beta + '\n\n'
                    # line_print += '\n***********************************\nmatch Photorec vs PE_Scan_beta \n***********************************'
                    # line_print += Fullfilename_pe_beta, Pe_Blob_beta

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

# data_pe_scan_beta = Lobotomy.get_databasedata('Filename,Pe_Blob', 'pe_scanner_beta', database)
    for line_pe_scan_beta in data_pe_scan_beta:
        pe_scan_beta_filename, pe_scan_beta_pe_blob = line_pe_scan_beta
        for test_clam in pe_scan_beta_pe_blob:
            if 'clamav' in test_clam:
                clam_line = test_clam.split(':')
                if clam_line[2] != 'OK':
                    cprint += clam_line

#
#

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


    # data_modscan = Lobotomy.get_databasedata('offset,name,base,size,file', 'modscan', database)
    # data_psxview = Lobotomy.get_databasedata('offset,name,pid,pslist,psscan,thrdproc,pspcid,csrss'
    #                                          'session,deskthrd,exittime', 'psxview', database)
    # data_psscan = Lobotomy.get_databasedata('offset,name,pid,ppid,pdb,timecreated,timeexited', 'psscan', database)



#loadpathpath, loadpathprocess, initpathpathh, initpathprocess, mempathpath, mempathprocess

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

            # line_print += '\n***********************************\nEmpty Ldr_Mappedpath and Ldr_ininit is False: Alert \n***********************************'
            # line_print += line_ldrmodules
        if ldr_loadpathpath != ldr_initpathpath or ldr_loadpathpath != ldr_mempathpath or ldr_mempathpath != ldr_initpathpath:
            if ldr_ininit == 'True' and ldr_inload == 'True' and ldr_inmem == 'True':
                # line_print += '\n***********************************\n' \
                #       'Non matching Paths, inmem, ininit and inload while Inload, Inmem and Ininit are True: Alert ' \
                #       '\n***********************************'
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
#                line_print += line_ldrmodules

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
    print sprint
    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(sprint)
        f.close()
    except:
        pass


#########################################################################################
#########################################################################################
# Done
#########################################################################################
#   Find unlinked dll's with ldrmodules. (inload, Ininit, Inmem = false)
# SELECT * FROM `ldrmodules_v` WHERE mappedpath = '' AND inmem = 'False';
#########################################################################################
#########################################################################################


#
#   - If Process in Mappedpath and Ininit = false, ignore.
#   - (Art of memory forensics, page 238, you never find the process exe in the init order list.)
#########################################################################################
#########################################################################################
# Done
#########################################################################################
#   - alert if ininit is false and mappedpath is empty!
# SELECT * FROM `ldrmodules_v` WHERE mappedpath = '' AND ininit = 'False';
#########################################################################################
#########################################################################################

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
