__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

# 03-07: WV -   Initiele aanmaak ico reader.


import sys
import main
import os
Lobotomy = main.Lobotomy()
plugin = "ioc"

DEBUG = False


def main():
    # Lobotomy.plugin_start(plugin, database)
    # Lobotomy.plugin_pct(plugin, database, 1)
    # case_settings = Lobotomy.get_settings(database)
    # imagename = case_settings["filepath"]
    # imagetype = case_settings["profile"]
    # casedir = case_settings["directory"]
    
    folder = 'ioc'

    scrptPth = os.path.dirname(os.path.realpath(__file__)) + "/" + folder

    files = ''
    for root, dirs, files in os.walk(scrptPth):
        for filename in files:
            filename = os.path.join(root, filename)
            if filename.endswith('.ioc'):
                table = ''
                data_ioc_definitions = Lobotomy.get_databasedata('IndicatorItem_id, ioc_definitions', 'lobotomy')
                data_ioc = Lobotomy.get_databasedata('iocid', 'ioc', 'lobotomy')
                iocid = ''
                last_modified = ''
                short_description = ''
                description = ''
                keywords = ''
                authored_by = ''
                authored_date = ''
                links = ''
                Indicator_operator = ''
                Indicator_operator_id = ''
                IndicatorItem_id = ''
                condition = ''
                Context_document = ''
                Context_document_type = ''
                Content_type = ''
                Content_type_Content = ''

                with open(filename) as f:
                    for line in f:
                        item_exits = '0'
                        item_exits_def = '0'
                        line = line.strip('\n')
                        # Lees IOC kop
                        if '<ioc xmlns:' in line:
                            lengte = len(line)
                            a = 0
                            for a in range(lengte-4):
                                if line[a:a+4] == 'id="':
                                    iocid = line[a:a+41].split('"')[1]
                                if line[a:a+14] == 'last-modified=':
                                    last_modified = line[a:a+35].split('"')[1]
                        if '<short_description>' in line:
                            short_description = line.split('>')[1].split('<')[0]
                        if '<description>' in line:
                            description = line.split('>')[1].split('<')[0]
                        if '<keywords>' in line:
                            keywords = line.split('>')[1].split('<')[0]
                        if '<authored_by>' in line:
                            authored_by = line.split('>')[1].split('<')[0]
                        if '<authored_date>' in line:
                            authored_date = line.split('>')[1].split('<')[0]
                        if '<links>' in line:
                            links = line.split('>')[1].split('<')[0]
                        if '<definition>' in line:
                            IOCHead = iocid, last_modified, short_description, description, keywords, authored_by, \
                                      authored_date, links
                            for item in range(len(data_ioc)):
                                print type(item) # return data is tuple.
                                print data_ioc(item), iocid
                                if iocid == item:
                                    item_exits = '1'
                            if item_exits == '0':
                                sql_line_start = "INSERT INTO ioc VALUES (0, "
                                sqlitem = ''
                                for item in IOCHead:
                                    sqlitem = sqlitem + "'{}',".format(item)
                                sql_line = sql_line_start + sqlitem[:-1] + ")"
                                Lobotomy.exec_sql_query(sql_line, 'lobotomy')


                        # less IOC body
                        if '<Indicator operator=' in line:
                            Indicator_operator = line.split('"')[1].split('"')[0]
                            if 'id="' in line:
                                Indicator_operator_id = line.split('"')[3].split('"')[0]
                        if '<IndicatorItem id=' in line:
                            IndicatorItem_id = line.split('"')[1].split('"')[0]
                            if 'condition="' in line:
                                condition = line.split('"')[3].split('"')[0]
                        if 'Context document=' in line:
                            Context_document = line.split('"')[1].split('"')[0]
                            if 'type="' in line:
                                Context_document_type = line.split('"')[3].split('"')[0]
                        if '<Content type=' in line:
                            Content_type = line.split('"')[1].split('"')[0]
                            Content_type_Content = line.split('>')[1].split('<')[0]
                            IOCBody = iocid, Indicator_operator, Indicator_operator_id, IndicatorItem_id, condition,\
                                      Context_document, Context_document_type, Content_type, Content_type_Content
                            #
                            # Prevent IOCBody duplicates in database
                            # print_data(IOCBody)
                            for item in data_ioc_definitions:
                                if IndicatorItem_id == item:
                                    item_exits_def = '1'
                            if item_exits_def == '0':

                            #if IndicatorItem_id not in data_ioc_definitions:
                                sql_line_start = "INSERT INTO ioc_definitions VALUES (0, "
                                sqlitem = ''
                                for item in IOCBody:
                                    sqlitem = sqlitem + "'{}',".format(item)
                                sql_line = sql_line_start + sqlitem[:-1] + ")"
                                Lobotomy.exec_sql_query(sql_line, 'lobotomy')

if __name__ == "__main__":
    main()
    # if len(sys.argv) != 1:
    #     print "Usage: " + plugin + ".py <databasename>"
    # else:
    #     main(sys.argv[1])
