__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script version    0.5
# Plugin version:   1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           impscan
# Edit:             14 sep 2015
# Detail:           Needed for Threatindex


import sys
import commands
import main
Lobotomy = main.Lobotomy()
plugin = "impscan"

DEBUG = False


def main(database):
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f {} --profile={} {}".format(imagename, imagetype, plugin)

    if DEBUG:
        print "Write log: (" + casedir + ", Database: " + database + " Start: Parsing volatility output: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir, " Database: " + database + " Start: Parsing volatility output: " + plugin)


    try:
        data_ldrmod = Lobotomy.get_databasedata('pid,process,base,inload,ininit,inmem,mappedpath,loadpathpath,'
                                                'loadpathprocess, initpathpath, initpathprocess, mempathpath,'
                                                'mempathprocess', 'ldrmodules_v', database)
    except:
        print 'Fail to get data from database'

    try:
        data_impscan = []
        for line_ldrmodules in data_ldrmod:
            ldr_pid, ldr_process, ldr_base, ldr_inload, ldr_ininit, ldr_inmem, ldr_mappedpath, ldr_loadpathpath, \
            ldr_loadpathprocess, ldr_initpathpath, ldr_initpathprocess, ldr_mempathpath, ldr_mempathprocess = line_ldrmodules
            if ldr_mappedpath == '' and ldr_ininit == 'False':
                print '\n***********************************'
                print 'Possible unlinked Dll found'
                print 'Empty Ldr_Mappedpath and Ldr_ininit is False, Getting imports from process.'
                print '***********************************'
                print 'Process         : ' + ldr_process
                print 'Base            : ' + ldr_base
                print 'Pid Ldrmodules  : ' + str(ldr_pid)
                tmp = ldr_process, ldr_pid, ldr_base
                data_impscan.append(tmp)
    except:
        data_impscan = ''
        print 'error parsing items'



#
# First, get a list of the pids. second get a list of all the base of the pids.
# We can get both from ldr modules. thats why we need to run AFTER ldrmodules.
# We need to build a check if ldrmodules have been run.
# We can get a list of dlllist, but that list is very large.
# Below we have a sample of ldrmodules.

# Getting a list of de pid, name and base is fine

# 680 	lsass.exe 	0x01000000 	True 	False 	True 	\WINDOWS\system32\lsass.exe
# 868 	lsass.exe 	0x00080000 	False 	False 	False
# 868 	lsass.exe 	0x7c900000 	True 	True 	True 	\WINDOWS\system32\ntdll.dll
# 868 	lsass.exe 	0x77e70000 	True 	True 	True 	\WINDOWS\system32\rpcrt4.dll
# 868 	lsass.exe 	0x7c800000 	True 	True 	True 	\WINDOWS\system32\kernel32.dll
# 868 	lsass.exe 	0x77fe0000 	True 	True 	True 	\WINDOWS\system32\secur32.dll
# 868 	lsass.exe 	0x7e410000 	True 	True 	True 	\WINDOWS\system32\user32.dll
# 868 	lsass.exe 	0x01000000 	True 	False 	True
# 868 	lsass.exe 	0x77f10000 	True 	True 	True 	\WINDOWS\system32\gdi32.dll
# 868 	lsass.exe 	0x77dd0000 	True 	True 	True 	\WINDOWS\system32\advapi32.dll
# 1928 	lsass.exe 	0x00080000 	False 	False 	False
# 1928 	lsass.exe 	0x7c900000 	True 	True 	True 	\WINDOWS\system32\ntdll.dll
# 1928 	lsass.exe 	0x773d0000 	True 	True 	True 	\WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll


# We can also grab the vadinfo of the base.

# python vol.py -f stuxnet.vmem --profile=WinXPSP3x86 vadinfo
# -p 1928,868,680 --addr=0x01000000
# Volatility Foundation Volatility Framework 2.4
# ************************************************************************
# Pid:
# 680
# VAD node @ 0x81db03c0 Start 0x01000000 End 0x01005fff Tag Vad
# Flags: CommitCharge: 1, ImageMap: 1, Protection: 7
# Protection: PAGE_EXECUTE_WRITECOPY
# ControlArea @823e4008 Segment e1735398
# NumberOfSectionReferences:
# 3 NumberOfPfnReferences:
# 4
# NumberOfMappedViews:
# 1 NumberOfUserReferences:
# 4
# Control Flags: Accessed: 1, File: 1, HadUserReference: 1, Image: 1
# FileObject @82230120, Name: \WINDOWS\system32\lsass.exe
# First prototype PTE: e17353d8 Last contiguous PTE: fffffffc
# Flags2: Inherit: 1
# ************************************************************************


#
# willem@lapto-01:/srv/lobotomy/dumps/TW6AKQY7IM63$ vol.py -f stuxnet.vmem impscan  -b 0x01000000 -p 1928
# Volatility Foundation Volatility Framework 2.4
# IAT        Call       Module               Function
# ---------- ---------- -------------------- --------
# 0x01002000 0x77dfb8af ADVAPI32.dll         LookupPrivilegeValueW
# 0x01002004 0x77ddeffc ADVAPI32.dll         AdjustTokenPrivileges
# 0x01002008 0x77dd797b ADVAPI32.dll         OpenProcessToken
# 0x01002014 0x7c81cafa kernel32.dll         ExitProcess
# 0x01002018 0x7c802530 kernel32.dll         WaitForSingleObject
# 0x0100201c 0x7c8449fd kernel32.dll         SetUnhandledExceptionFilter
# 0x01002020 0x7c80ac9f kernel32.dll         SetErrorMode
# 0x01002024 0x7c809bd7 kernel32.dll         CloseHandle
# 0x01002028 0x7c80de85 kernel32.dll         GetCurrentProcess
# 0x0100202c 0x7c8106c7 kernel32.dll         CreateThread
# 0x01002030 0x7c801e1a kernel32.dll         TerminateProcess
# 0x01002034 0x7c801ad4 kernel32.dll         VirtualProtect
# 0x01002038 0x7c80e4cd kernel32.dll         GetModuleHandleW
# 0x0100203c 0x7c8097b8 kernel32.dll         GetCurrentThreadId
# 0x01002040 0x7c80932e kernel32.dll         GetTickCount
# 0x01002044 0x7c80baf4 kernel32.dll         lstrcpyW
# 0x01002048 0x7c809a99 kernel32.dll         lstrlenW
# 0x0100204c 0x7c80ae30 kernel32.dll         GetProcAddress
# 0x01002054 0x7e41a9b6 USER32.dll           wsprintfW
# 0x01002fe6 0x7c80ba04 kernel32.dll         UnmapViewOfFile      # The ZwUnmapViewOfSection or NtUnmapViewOfSection
#                                                                 WIN32 API function may be used to unmap the original code:
# 0x01002ff6 0x7c90d160 ntdll.dll            ZwCreateSection
# 0x01002ffa 0x7c90d500 ntdll.dll            ZwMapViewOfSection
# 0x0100300a 0x7c90cfd0 ntdll.dll            ZwClose

  # 254  vol.py -f stuxnet.vmem impscan --BASE 0x01000000 -p 1928 -s 0x6000
  # 255  vol.py -f stuxnet.vmem impscan -b 0x01000000 -p 1928 -s 0x6000

    items = []
    for process, pid, base in data_impscan:
        command = "vol.py -f {} --profile={} {} -b {} -p {}".format(imagename, imagetype, plugin, base, pid)
        if DEBUG:
            print "Write log: " + database + ", Start: " + command
            print "Write log: " + casedir + ", Start: " + command
        else:
            Lobotomy.write_to_main_log(database, " Start: " + command)
            Lobotomy.write_to_case_log(casedir, " Start: " + command)

        if DEBUG:
            print "Write log: " + database + " Stop: " + command
            print "Write log: " + casedir + " Stop: " + command
        else:
            Lobotomy.write_to_case_log(casedir, " Stop : " + command)

        if DEBUG:
            print command
        else:
            print "Running Volatility -", plugin, ", please wait."
            print command
            vollog = ""
            status, vollog = commands.getstatusoutput(command)
        try:
            f = open(imagename + '-' + plugin + '-' + pid + '-' + base + '.txt', 'w')
            f.write(vollog)
            f.close()
        except:
            pass

        for item in vollog.split('\n'):
            if not item.startswith('Volatility'):
                if not item.startswith('IAT'):
                    if not item.startswith('---'):
                        # test = item.split(' ')
                        # lenline = []
                        # lencount = 0
                        # for tmp in test:
                        #     print tmp, test, len(tmp), lencount
                        #     lenline[lencount] = len(tmp)
                        #     lencount += 1
                        test = item.split(' ')
                        imptmp = ''
                        for a in test:
                            if a != '':
                                imptmp += a + ' '
                        tmp = process + ' ' + str(pid) + ' ' + str(base) + ' ' + str(imptmp[:-1])

                        #items.append(tmp)
                        sql_cmd = ''
                        line = tmp.split(' ')
                        for sql_item in line:
                            sql_cmd += ", '{}'".format(sql_item)

                        sqlq = "INSERT INTO " + plugin + " VALUES (0" + sql_cmd + ")"
                        try:
                            Lobotomy.exec_sql_query(sqlq, database)
                        except:
                            print 'SQL Error in ', database, 'plugin: ', plugin
                            print 'SQL Error: ',  sqlq


                        print tmp
#                    print item

    # print 'Parsing ' + plugin + ' data...'
    # for item in items:
    #     tmp = ''
    #     # for impscandata in item[3]:
    #     #     tmp += impscandata + ' '
    #     # line = str(item) + ' ' + str(tmp)
    #     # print line
    #     sql_cmd = ''
    #     # for sql_item in item:
    #     #     sql_cmd += ", '{}'".format(sql_item)
    #     line = item.split(' ')
    #     for sql_item in line:
    #         sql_cmd += ", '{}'".format(sql_item)
    #
    #     sqlq = "INSERT INTO " + plugin + " VALUES (0" + sql_cmd + ")"
    #     try:
    #         Lobotomy.exec_sql_query(sqlq, database)
    #     except:
    #         print 'SQL Error in ', database, 'plugin: ', plugin
    #         print 'SQL Error: ',  sqlq
    #         # Lobotomy.write_to_case_log(casedir, "Database: " + database + " Error:  running plugin: " + plugin)
    #         # Lobotomy.write_to_case_log(casedir, "Database: " + database + 'SQL line: ' + sqlq)

#process,pid,base,IAT, Call,Module,Function



        #
        #
        # try:
        #     if pct != pcttmp:
        #         print "plugin: " + plugin + " - Database: " + database + " - pct done: " + str(pct)
        #         Lobotomy.plugin_pct(plugin, database, pct)
        # except:
        #     pass
        # pcttmp = pct

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
