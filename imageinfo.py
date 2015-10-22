#!/usr/bin/env python
###
### 03-02: WV - Aanpassen SQL query tbv modificatie website en database
###
###
### 12-02: WV - Image info opnemen in de database als 'plugin'
###
###
### 18-02: WV - Met Windows 7 64 bits wordt het verkeerde profiel gekozen.
###             oorzaak: loop door de gevonden servicepacks. Win7SP1 en Win2008SP1.
###             Oplossing: counter ertussen gezet: count =
###             Oplossing moet nog getest worden met Windows 8 en Win2008
###

# Todo
# Try to filter with grep?
# wcm://Microsoft-Windows-OS-Kernel?version=6.1.7600.16385
# WCM://MICROSOFT-WINDOWS-OS-KERNEL?VERSION=6.1.7600.16792&LANGUAGE=NEUTRAL&PROCESSORARCHITECTURE=AMD64&PUBLICKEYTOKEN=31BF3856AD364E35&VERSIONSCOPE=NONSXS&SCOPE=ALLUSERS

# Windows 10
# -------------------------
# Volatility Foundation Volatility Framework 2.4
# Traceback (most recent call last):
#   File "/home/solvent/lob_scripts/imageinfo.py", line 73, in <module>
#     imageinfo(sys.argv[1])
#   File "/home/solvent/lob_scripts/imageinfo.py", line 55, in imageinfo
#     sp = 'SP{}'.format(servicepack)
# UnboundLocalError: local variable 'servicepack' referenced before assignment
# ID: 21
# Command: python /home/solvent/lob_scripts/multiparser.py 1510221123_Win7Sp1X64_Cleanraw clipboard
# Priority: 2


import os
import re
import sys
import time
import main
plugin = 'imageinfo'
Lobotomy = main.Lobotomy()


def imageinfo(database):
    settings = Lobotomy.get_settings(database)
    Lobotomy.plugin_start(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 1)
    Lobotomy.write_to_main_log(database, "Starting 'imageinfo' plugin...")
    Lobotomy.write_to_case_log(settings['directory'], "Starting 'imageinfo' plugin...")
    command = 'vol.py -f "{}" imageinfo > {}/imageinfo.txt'.format(settings['filepath'], settings['directory'])
    Lobotomy.write_to_case_log(settings['directory'], "Executing command imageinfo")
    Lobotomy.write_to_case_log(settings['directory'], "EXEC: {}".format(command))
    os.system(command)
    Lobotomy.write_to_case_log(settings['directory'], "Command imageinfo executed")
    counter = 1
    servicepack = profiles = ''
    with open(settings['directory'] + '/imageinfo.txt') as f:
        for line in f:
            if not line.startswith("Determining") and line != "\n":
                SQL_cmd = "INSERT INTO imageinfo VALUES (0, '{}', '{}')".format(
                    line.split(' : ')[0], line.split(' : ')[1])
                Lobotomy.exec_sql_query(SQL_cmd, database)
            if 'Suggested Profile(s)' in line:
                profiles = line.split(':')[1].strip()
                profiles = re.sub(r'\([^)]*\)', '', profiles)
                Lobotomy.write_to_case_log(settings['directory'], "Found possible profiles: {}".format(profiles))
            if 'Image Type (Service Pack)' in line:
                servicepack = line.split(':')[1].strip()
                Lobotomy.write_to_case_log(settings['directory'], "Found service pack: {}".format(servicepack))
            counter += 1
    count = 0
    for x in profiles.strip().split(','):
        sp = 'SP{}'.format(servicepack)
        if sp in x:
            x = x.replace(' ', '')
            if count == 0:
                Lobotomy.write_to_case_log(settings['directory'], "Possible match: {}. Inserting in database..".format(x))
                Lobotomy.write_to_main_log(database, "Imageinfo found a possible match: {}. Inserting in database..".format(x))
                Lobotomy.exec_sql_query("UPDATE settings SET profile='{}'".format(x), database)
                count = 1
    Lobotomy.write_to_case_log(settings['directory'], "Stopping 'imageinfo' plugin...")
    Lobotomy.write_to_main_log(database, "Stopping 'imageinfo' plugin...")
    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: imageinfo.py [Database]"
    else:
        imageinfo(sys.argv[1])