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



import os
import re
import sys
import time
import main

Lobotomy = main.Lobotomy()


def imageinfo(database):
    settings = Lobotomy.get_settings(database)
    Lobotomy.write_to_main_log(database, "Starting 'imageinfo' plugin...")
    Lobotomy.write_to_case_log(settings['directory'], "Starting 'imageinfo' plugin...")
    command = 'vol.py -f "{}" imageinfo > {}/imageinfo.txt'.format(settings['filepath'], settings['directory'])
    Lobotomy.write_to_case_log(settings['directory'], "Executing command imageinfo")
    Lobotomy.write_to_case_log(settings['directory'], "EXEC: {}".format(command))
    os.system(command)
    Lobotomy.write_to_case_log(settings['directory'], "Command imageinfo executed")
    counter = 1
    with open(settings['directory'] + '/imageinfo.txt') as f:
        for line in f:
            if not line.startswith("Determining") and line != "\n":
                omschrijving = line[0:30].strip("  ")
                waarde = line[33:].strip("\n")
                SQL_cmd = "INSERT INTO imageinfo VALUES (0, '{}', '{}')".format(omschrijving, waarde)
                Lobotomy.exec_sql_query(SQL_cmd, database)
            if counter == 3:
                profiles = line.split(':')[1].strip()
                profiles = re.sub(r'\([^)]*\)', '', profiles)
                Lobotomy.write_to_case_log(settings['directory'], "Found possible profiles: {}".format(profiles))
            elif counter == 10:
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: imageinfo.py [Database]"
    else:
        imageinfo(sys.argv[1])