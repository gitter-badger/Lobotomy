# coding=utf-8
__author__ = 'Wim Venhuizen'

#
# Script version    0.5
# Plugin version:   1
# 08 mrt 2015:      Wim Venhuizen
# Plugin:           Lobotomy Treat scanner
#
# Eerste opzet voor treatindex
#
# Date:             08-07-2015
# Script haalt niet meer de hele lijst met hashes op, maar controleerd in de database of een hash bestaat.
#
# 08 mrt 2015:      Wim Venhuizen
#  Detail:          Add moddump to the scanner


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
    print 'start-time: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #bad_hashes = Lobotomy.get_databasedata('md5hash,added', 'bad_hashes', 'lobotomy')
    data_dlldump = Lobotomy.get_databasedata('fullfilename,modulename,filename,md5', 'dlldump', database)
    data_moddump = Lobotomy.get_databasedata('fullfilename,modulename,filename,md5', 'dlldump', database)
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
    print 'Comparing bad_hashed with hashes from image, please wait.'

    # Compare the hash from ddldump, procdump and photorec with the hashes in the database, bad_hashes
    # if there is no match, there will be no trigger for the program to collect data.

    for line_dlldump in data_dlldump:
        fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump = line_dlldump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_dlldump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_dlldump:
                    print 'Match - Volatility plugin: Dlldump. :', md5hash_dlldump
                    bad_hashes_list.append(['dlldump', fullfilename_dlldump, modulename_dlldump, filename_dlldump, md5hash_dlldump])

    for line_moddump in data_moddump:
        fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump = line_moddump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_moddump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_moddump:
                    print 'Match - Volatility plugin: Moddump. :', md5hash_moddump
                    bad_hashes_list.append(['moddump', fullfilename_moddump, modulename_moddump, filename_moddump, md5hash_moddump])

    for line_procdump in data_procdump:
        fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump = line_procdump
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_procdump.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_procdump:
                    print 'Match - Volatility plugin: Procdump. :', md5hash_procdump
                    bad_hashes_list.append(['procdump', fullfilename_procdump, name_procdump, filename_procdump, md5hash_procdump])
    for line_photorec in data_photorec:
        fullfilename_photorec, md5hash_photorec = line_photorec
        sql_prefix = "bad_hashes where md5hash = '{}'".format(md5hash_photorec.strip('\n'))
        get_hash_from_db_tuple = Lobotomy.get_databasedata('md5hash', sql_prefix, 'lobotomy')
        for get_hash_from_db in get_hash_from_db_tuple:
            for db_hash in get_hash_from_db:
                if db_hash == md5hash_photorec:
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
            print '\n***********************************\nEmpty Ldr_Mappedpath and Ldr_ininit is False: Alert \n***********************************'
            print line_ldrmodules
        if ldr_loadpathpath != ldr_initpathpath or ldr_loadpathpath != ldr_mempathpath or ldr_mempathpath != ldr_initpathpath:
            if ldr_ininit == 'True' and ldr_inload == 'True' and ldr_inmem == 'True':
                print '\n***********************************\n' \
                      'Non matching Paths, inmem, ininit and inload while Inload, Inmem and Ininit are True: Alert ' \
                      '\n***********************************'
                print line_ldrmodules


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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <database>"
    else:
        main(sys.argv[1])
