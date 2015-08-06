__author__ = 'Wim Venhuizen'

#
# Script.version    0.1
# Date:             08-03-2015
# Edited:           W Venhuizen
#
# Eerste opzet voor treatindex
#

import os
import sys
import main
import commands
import time
from datetime import datetime

Lobotomy = main.Lobotomy()
plugin = "treatindex"

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
    print 'Reading Database, please wait'
    print 'Script can run more then 30 minutes before its finished'
    print 'start-time: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bad_hashes = Lobotomy.get_databasedata('md5hash,added', 'bad_hashes', 'lobotomy')
    data_dlldump = Lobotomy.get_databasedata('fullfilename,modulename,filename,md5', 'dlldump', database)
    data_procdump = Lobotomy.get_databasedata('fullfilename,name,filename,md5', 'procdump', database)
    data_photorec = Lobotomy.get_databasedata('fullfilename,filemd5', 'photorec', database)
    data_vol_yara = Lobotomy.get_databasedata('owner_name,pid', 'volatility_yarascan', database)
    data_yara = Lobotomy.get_databasedata('filename,string,yara,yara_description', 'yarascan', database)
    data_exifinfo = Lobotomy.get_databasedata('Filename,Exifinfo', 'exifinfo', database)
    data_pe_scan = Lobotomy.get_databasedata('Fullfilename,Pe_Compiletime,Pe_Packer,Filetype,Original_Filename,Yara_Results', 'pe_scan', database)
    data_pe_scan_beta = Lobotomy.get_databasedata('Filename,Pe_Blob', 'pe_scanner_beta', database)

    bad_hashes_list = []
    stoptime = time.time()
    print 'seconds to read database(s)', round(stoptime - starttime)
    starttime = time.time()
    print 'start-time: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'Reading hashes from database'
    print 'And comparing bad_hashed with hashes from image, please wait.'

    # Looking for a match where bad_hashed is the source.
    # Compare the bad_hash with ddldump, procdump and photorec.
    # if there is no match, there will be no trigger for the program to collect data.

    for a in bad_hashes:
        hashlist, b = a
        #bad_hashes_list.append(hashlist)
        for line_dlldump in data_dlldump:
            fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = line_dlldump
            if hashlist == md5hash_dlldump:
                print 'Match - Volatility plugin: Dlldump. :', md5hash_dlldump
                bad_hashes_list.append(['dlldump', fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump])
        for line_procdump in data_procdump:
            fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = line_procdump
            if hashlist == md5hash_procdump:
                print 'Match - Volatility plugin: Procdump. :', md5hash_procdump
                bad_hashes_list.append(['procdump', fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump])
        for line_photorec in data_photorec:
            fullfilename_photorec, md5hash_photorec = line_photorec
            if hashlist == md5hash_photorec:
                print 'Match - Lobotomy plugin: Photorec. :', md5hash_photorec
                bad_hashes_list.append(['photorec', fullfilename_photorec, md5hash_photorec])

    # bad_hashes_list.append(['dlldump', '/home/solvent/dumps/HPC62ZEFP5EK/dump/module.624.1fa5650.1000000.dll',
    #                          'winlogon.exe', 'module.624.1fa5650.1000000.dll', '3365db5fe22fca0eb673f4da22dedb3d'])
    # bad_hashes_list.append(['procdump', '/home/solvent/dumps/HPC62ZEFP5EK/dump/executable.624.exe',
    #                         'winlogon.exe', 'executable.624.exe', '3365db5fe22fca0eb673f4da22dedb3d'])
    # bad_hashes_list.append(['photorec', '/home/solvent/dumps/HPC62ZEFP5EK/photorec_dump.1/f0020072.exe',
    #                         '00fa7854f212fcbfe8586f42186bc1d9'])

    stoptime = time.time()
    print 'seconds to compare hashes database(s)', round(stoptime - starttime)

    # Collect data where dlldump is the source (md5).

    for item in bad_hashes_list:
        if item[0] == 'dlldump':
            a, fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = item
            pid_dlldump = filename_dlldump.split('.')[1]
            print fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump, pid_dlldump
            for line_vol_yara in data_vol_yara:
                ownername_vol_yara, pid_vol_yara = line_vol_yara
                if str(pid_vol_yara) == str(pid_dlldump):
                    print '\n\n\n***********************************\nmatch DLLDump vs volatility_Yara \n***********************************'
                    print fullfilename_dlldump, modulename_dlldump, filename_dlldump, pid_dlldump
                    print ownername_vol_yara, pid_vol_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_dlldump:
                    print '\n***********************************\nmatch DLLDump vs Exifinfo \n***********************************'
                    print "Exifinfo filename \t\t:", filename_exifinfo
                    print exifinfo

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_dlldump:
                    print '\n***********************************\nmatch DLLDump vs PE_Scan \n***********************************'
                    print Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_dlldump:
                    print '\n***********************************\nmatch DLLDump vs PE_Scan_beta \n***********************************'
                    print Fullfilename_pe_beta, Pe_Blob_beta


        # Collect data where procdump is the source (md5).

        if item[0] == 'procdump':
            a, fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = item
            pid_procdump = filename_procdump.split('.')[1]
            print fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump, pid_procdump
            for line_vol_yara in data_vol_yara:
                ownername_vol_yara, pid_vol_yara = line_vol_yara
                if str(pid_vol_yara) == str(pid_procdump):
                    print '\n\n\n***********************************\nmatch ProcDump vs volatility_Yara \n***********************************'
                    print fullfilename_procdump, name_procdump, filename_procdump, pid_procdump
                    print ownername_vol_yara, pid_vol_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_procdump:
                    print '\n***********************************\nmatch ProcDump vs Exifinfo \n***********************************'
                    print "Exifinfo filename \t\t:", filename_exifinfo
                    print exifinfo

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_procdump:
                    print '\n***********************************\nmatch ProcDump vs PE_Scan \n***********************************'
                    print Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_procdump:
                    print '\n***********************************\nmatch ProcDump vs PE_Scan_beta \n***********************************'
                    print Fullfilename_pe_beta, Pe_Blob_beta


        # Collect data where photorec is the source (md5).

        if item[0] == 'photorec':
            a, fullfilename_photorec, md5hash_photorec = item
            print fullfilename_photorec, md5hash_photorec
            for line_yara in data_yara:
                filename_yara, string_yara, yara_yara, yara_description_yara = line_yara
                if filename_yara == fullfilename_photorec:
                    print '\n\n\n***********************************\nmatch Photorec vs Yara \n***********************************'
                    print fullfilename_photorec, md5hash_photorec
                    print filename_yara, string_yara, yara_yara, yara_description_yara

            for line_exifinfo in data_exifinfo:
                filename_exifinfo,exifinfo = line_exifinfo
                if filename_exifinfo == fullfilename_photorec:
                    print '\n***********************************\nmatch Photorec vs Exifinfo \n***********************************'
                    print "Exifinfo filename \t\t:", filename_exifinfo
                    print exifinfo

            for line_pe_scan in data_pe_scan:
                Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe = line_pe_scan
                if Fullfilename_pe == fullfilename_photorec:
                    print '\n***********************************\nmatch Photorec vs PE_Scan \n***********************************'
                    print Fullfilename_pe, Pe_Compiletime, Pe_Packer, Filetype_pe, Original_Filename_pe, Yara_Results_pe

            for line_pe_scan_beta in data_pe_scan_beta:
                Fullfilename_pe_beta,Pe_Blob_beta = line_pe_scan_beta
                if Fullfilename_pe_beta == fullfilename_photorec:
                    print '\n***********************************\nmatch Photorec vs PE_Scan_beta \n***********************************'
                    print Fullfilename_pe_beta, Pe_Blob_beta




#   Bron:   volatility-yara
#           ownername
#           PID




    #Lobotomy.plugin_stop(plugin, database)
    #Lobotomy.plugin_pct(plugin, database, 100)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <database>"
    else:
        main(sys.argv[1])

