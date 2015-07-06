__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

#
# Script.version    0.1
# Date:             06-07-2015
# Edited:           W Venhuizen
#
# Date:             06-05-2015:
# Eerste opzet yarascan voor lobotomy.
#

import sys
import main
import commands

Lobotomy = main.Lobotomy()
plugin = "Yarascan"

DEBUG = False


def main(database, filename):
    command = "yara /home/solvent/lob_scripts/yara_rules/index.yara " + filename + " -m -s"
    print "Running yarascan on file: " + filename
    log = ""
    status, log = commands.getstatusoutput(command)
    counter = 0
    b = ''
    c = ''
    for item in log.split('\n'):
        if item.endswith(filename):
            counter += 1
            b = item.split('[')[0]
            if 'description' in item:
                c = item[int(item.find('description')+13):].split('"')[0]
        else:
            a = item.split(':')
            try:
                offset = a[0]
            except:
                offset = ''
            try:
                decription = a[1]
            except:
                decription = ''
            try:
                string = a[2]
            except:
                string = ''
            print filename, offset, decription, string, b, c


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + plugin + ".py <databasename> filename"
    else:
        main(sys.argv[1], sys.argv[2])

# solvent@lobotomy:~/lob_scripts/ZooKeeper-master$ yara /home/solvent/lob_scripts/ZooKeeper-master/data/yara_rules/index.yara /home/solvent/dumps/9XYG67O08Z3T/photorec_dump.1/f0183240.dll -m -s
# embedded_macho [author="nex",description="Contains an embedded Mach-O file"] /home/solvent/dumps/9XYG67O08Z3T/photorec_dump.1/f0183240.dll
# 0x10382:$magic1: CA FE BA BE
# 0x1056f:$magic1: CA FE BA BE
# 0x10973:$magic1: CA FE BA BE
# 0x10f2a:$magic1: CA FE BA BE
# 0x21d9a:$magic1: CA FE BA BE
# 0x22875:$magic1: CA FE BA BE
# 0x22d92:$magic1: CA FE BA BE
# 0x236b5:$magic1: CA FE BA BE
# 0x2c41b:$magic1: CA FE BA BE
# 0x2c773:$magic1: CA FE BA BE
# 0x33bf8:$magic1: CA FE BA BE
# 0x3d6ce:$magic1: CA FE BA BE
# Stuxnet [description="Stuxnet",author="Wim Venhuizen",last_modified="2015-07-06"] /home/solvent/dumps/9XYG67O08Z3T/photorec_dump.1/f0183240.dll
# 0x25dc3:$string1: mrx
# 0x2623f:$string1: mrx
# 0x26529:$string1: mrx
# 0x26937:$string1: mrx
# 0xd44a:$file4: oem7A.PNF
# 0xd4f4:$file4: oem7A.PNF
# 0xd5a2:$file4: oem7A.PNF
# 0xd644:$file4: oem7A.PNF
# 0x25dc3:$file6: mrxcls.sys
# 0x2623f:$file6: mrxcls.sys
# 0x26529:$file6: mrxcls.sys
# 0x26937:$file6: mrxcls.sys
