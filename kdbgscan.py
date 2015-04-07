#!/usr/bin/env python
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
###

import os
import re
import sys
import time
import main

Lobotomy = main.Lobotomy()
plugin = "kdbgscan"

DEBUG = False


def main(database):
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    command = "vol.py -f " + imagename + " " + plugin + " > " + imagename + plugin + ".txt"
    
    if DEBUG:
        print "Write log: " + database + " ,Start: " + command
        print "Write log: " + casedir + " ,Start: " + command
    else:
        Lobotomy.write_to_main_log(database, " Start: " + command)
        Lobotomy.write_to_case_log(casedir, " Start: " + command)
        
    if DEBUG:
        print command
    else:
        os.system(command)
        
    if DEBUG:
        print "Write log: " + database + " ,Stop: " + command
        print "Write log: " + casedir + " ,Stop: " + command
    else:
        Lobotomy.write_to_main_log(database, " Stop : " + command)
        Lobotomy.write_to_case_log(casedir, " Stop : " + command)

    if DEBUG:
        print "Write log: (" + casedir + " ,Database: " + database + " Start:  running plugin: " + plugin + ")"
    else:
        Lobotomy.write_to_case_log(casedir,  "Database: " + database + " Start:  running plugin: " + plugin)
        
    try:
        print "open file: " + imagename + plugin + ".txt"
        with open(imagename + plugin + ".txt") as f:
            write_to_bd = []
            kdbg = 0
            offsetv = 0
            offsetp = 0
            kdbgowner = 0
            kdbgheader = 0
            version64 = 0
            sp = 0
            build = 0
            ActiveProcessoffset = 0
            ActiveProcess = 0
            LoadedModuleListoffset = 0
            LoadedModuleList = 0
            KernelBase = 0
            major = 0
            minor = 0
            kpcr = 0
            for line in f:
                #**************************************************
                #Instantiating KDBG using: Kernel AS WinXPSP3x86 (5.1.0 32bit)
                #Offset (V)                    : 0x80545b60
                #Offset (P)                    : 0x545b60
                #KDBG owner tag check          : True
                #Profile suggestion (KDBGHeader): WinXPSP2x86
                #Version64                     : 0x80545b38 (Major: 15, Minor: 2600)
                #Service Pack (CmNtCSDVersion) : 3
                #Build string (NtBuildLab)     : 2600.xpsp_sp3_gdr.100427-1636
                #PsActiveProcessHead           : 0x8055a1d8 (33 processes)
                #PsLoadedModuleList            : 0x80554040 (124 modules)
                #KernelBase                    : 0x804d7000 (Matches MZ: True)
                #Major (OptionalHeader)        : 5
                #Minor (OptionalHeader)        : 1
                #KPCR                          : 0xffdff000 (CPU 0)
                
                
                if line.startswith("Instantiating KDBG using"):
                    kdbg = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Offset (V)"):
                    offsetv = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Offset (P)"):
                    offsetp = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("KDBG owner tag check"):
                    kdbgowner = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Profile suggestion"):
                    kdbgheader = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Version64"):
                    version64 = line.strip("\n").split(":",1)[1].split(" ",1)[1]     
                if line.startswith("Service Pack"):
                    sp = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Build string"):
                    build = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("PsActiveProcessHead"):
                    ActiveProcessoffset, ActiveProcess = line.split(":")[1].strip(")\n").split("(")
                    ActiveProcessoffset = ActiveProcessoffset.split(" ")[1]
                if line.startswith("PsLoadedModuleList"):
                    LoadedModuleListoffset, LoadedModuleList = line.split(":")[1].strip(")\n").split("(")
                    LoadedModuleListoffset = LoadedModuleListoffset.split(" ")[1]
                if line.startswith("KernelBase"):
                    KernelBase = line.strip("\n").split(":",1)[1].split(" ",1)[1]
                if line.startswith("Major"):
                    major = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("Minor"):
                    minor = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("KPCR"):
                    kpcr = line.strip("\n").split(":")[1].split(" ",1)[1]
                if line.startswith("**********") and kdbg != 0:
                    SQL_cmd = "INSERT INTO kdbgscan VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(kdbg, offsetv, offsetp, kdbgowner, kdbgheader, version64, sp, build, ActiveProcessoffset, ActiveProcess, LoadedModuleListoffset, LoadedModuleList, KernelBase, major, minor, kpcr)
                    if DEBUG:
                        print SQL_cmd
                    else:
                        Lobotomy.exec_sql_query(SQL_cmd, database)
            
            SQL_cmd = "INSERT INTO kdbgscan VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(kdbg, offsetv, offsetp, kdbgowner, kdbgheader, version64, sp, build, ActiveProcessoffset, ActiveProcess, LoadedModuleListoffset, LoadedModuleList, KernelBase, major, minor, kpcr)
            if DEBUG:
                print SQL_cmd
            else:
                Lobotomy.exec_sql_query(SQL_cmd, database)

    except IOError:
        print "IOError, file not found."
        if DEBUG:
            print "Debug mode is on: try creating a sample file."



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])