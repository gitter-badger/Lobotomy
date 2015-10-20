__author__ = 'Wim Venhuizen, Jeroen Hagebeek'
#
# Script version    0.5
# Plugin version:   0.1
# 11 aug 2015:      Wim Venhuizen
# Plugin:           Netscan
# Edit:             16 okt 2015
# Detail:           Get the networkconnections from a memorydump
# Detail:           Needed for Report function


import sys
import main
from cStringIO import StringIO

Lobotomy = main.Lobotomy()

plugin = "netscan"

DEBUG = False


def main(database):
    import volatility.conf as conf
    import volatility.registry as registry
    registry.PluginImporter()
    import volatility.commands as commands
    import volatility.addrspace as addrspace
    config = conf.ConfObject()
    registry.register_global_options(config, commands.Command)
    registry.register_global_options(config, addrspace.BaseAddressSpace)
    # import volatility.debug as debug
    # import volatility.win32 as win32
    # import volatility.obj as obj
    # import volatility.utils as utils
    import volatility.plugins.netscan as netscan

    config.parse_options()
    config.PROFILE = ''
    config.LOCATION = ''

    Lobotomy.plugin_start(plugin, database)
    case_settings = Lobotomy.get_settings(database)
    imagename = case_settings["filepath"]
    imagetype = case_settings["profile"]
    casedir = case_settings["directory"]
    case = database
    log = ''
    config.PROFILE = imagetype
    config.LOCATION = 'file://' + imagename

    # Check if Profile is supported
    if imagetype.startswith('WinXP' or 'mac_' or 'linux_'):
        print '{} is not supported for {}'.format(plugin, imagetype)
        exit()

    print 'Running {}, please wait...'.format(plugin)
    p = netscan.Netscan(config)
    old_stdout = sys.stdout
    sys.stdout = volnetscan = StringIO()
    p.render_text(sys.stdout, p.calculate())
    sys.stdout = old_stdout

    voldata = volnetscan.getvalue().split('\n')

    # Writing log to casefolder
    try:
        f = open(imagename + '-' + plugin + '.txt', 'w')
        f.write(str(voldata))
        f.close()
    except:
        pass
    
    # Parsing data
    sql_list = []
    print 'Parsing {} data...'.format(plugin)
    for line in voldata:
        offsetp = proto = laddress = faddress = state = pid = owner = created = ''
        volplugindata = []
        if line != '' and not line.startswith('Offset'):
            offsetp = line[0:19].strip(' ') # Offset {0:<18}
            proto = line[19:28].strip(' ') # Proto {1:<8}
            laddress = line[28:59].strip(' ') # Local Address {2:<30}
            faddress = line[59:80].strip(' ') # Foreing Address {3:<20}
            state = line[80:97].strip(' ') # State {4:<16}
            pid = line[97:106].strip(' ') # Pid {5:<8}
            owner = line[106:121] # Owner {6:<14}
            created = line[121:] # Created {7}

            sql_cmd = ''
            sql_cmd = "INSERT INTO {} VALUES (0, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(plugin,
                                                    offsetp, proto, laddress, faddress, state, pid, owner, created)
            try:
                #print sql_cmd
                Lobotomy.exec_sql_query(sql_cmd, database)
            except:
                print 'SQL Error in ', database, 'plugin: ', plugin
                print 'SQL Error: ',  sql_cmd

    Lobotomy.plugin_stop(plugin, database)
    Lobotomy.plugin_pct(plugin, database, 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + plugin + ".py <databasename>"
    else:
        main(sys.argv[1])
