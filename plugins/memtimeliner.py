__author__ = 'Wim Venhuizen, Jeroen Hagebeek'

import sys
import os
import MySQLdb
import main
Lobotomy = main.Lobotomy()

DEBUG = False


def main(database):
	case_settings = Lobotomy.get_settings(database)
	imagename = case_settings["filepath"]
	imagetype = case_settings["profile"]
	casedir = case_settings["directory"]
	command =[]
	command.append("vol.py -f " + imagename + " --profile=" + imagetype + " timeliner --output=body --output-file=" +  imagename + "-timeliner_time")
 	command.append("vol.py -f " + imagename + " --profile=" + imagetype + " shellbags --output=body --output-file=" +  imagename + "-shellbagstime")
 	command.append("vol.py -f " + imagename + " --profile=" + imagetype + " mftparser --output=body --output-file=" +  imagename + "-mfttime")
	command.append("cat " +  imagename + "-timeliner_time " +  imagename + "-mfttime " +  imagename + "-shellbagstime >> " +  imagename + "-bodytimeline.txt")
	command.append("mactime -b " +  imagename + "-bodytimeline.txt -d > " + imagename + "-mactime.txt")

	if DEBUG:
		for item in command:
			print item
		#input_sql(imagename, database)
	else:
		for item in command:
			Lobotomy.write_to_main_log(database + " Start: " + item)
			Lobotomy.write_to_case_log(casedir,"Database: " + database + " Start: " + item)
			os.system(item)
			Lobotomy.write_to_main_log(database + " Stop : " + item)
			Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop : " + item)
		Lobotomy.write_to_main_log(database + " Start: Update database ")
		Lobotomy.write_to_case_log(casedir,"Database: " + database + " Start: Update database ")
		input_sql(imagename, database)
		Lobotomy.write_to_main_log(database + " Stop  : Update database")
		Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop : Update database")
#		Lobotomy.write_to_main_log("---------------------------------------")

#		Lobotomy.exec_sql_query
		

def input_sql(imagename, database):
		counter = 0
		with open(imagename + "-mactime.txt") as f:
			for line in f:
				if counter != 0:
					listitem = line.split(',')
					if DEBUG:
						print "VALUES {}, {}, {}, {}, {}, {}, {}, {}".format(listitem[0], listitem[1], listitem[2], listitem[3], listitem[4], listitem[5], listitem[6], listitem[7])
					else:
						Lobotomy.exec_sql_query("INSERT INTO memtimeliner (date, size, type, mode, uid, gid, meta, filename) \
											VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(listitem[0], listitem[1], listitem[2], listitem[3], listitem[4], listitem[5], listitem[6], listitem[7]),database)
						#sql = MySQLdb.connect('localhost', 'root', 'ZPRvLVaZReH5BbNJGCu7OeEO1edBaJzh', 'template')
						#cur = sql.cursor()
						#cur.execute("INSERT INTO memtimeliner (date, size, type, mode, uid, gid, meta, filename)"
						#					"VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(listitem[0], listitem[1], listitem[2], listitem[3], listitem[4], listitem[5], listitem[6], listitem[7]))
						#sql.commit()
						#sql.close()
				counter += 1


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: memtimeliner.py [database]"
	else:
		main(sys.argv[1])
