#!/usr/bin/env python

import re
#import MySQLdb
import sys
import main
import os

DEBUG = False

Lobotomy = main.Lobotomy()


def main(database, plugin):
	case_settings = Lobotomy.get_settings(database)
	imagename = case_settings["filepath"]
	imagetype = case_settings["profile"]
	casedir = case_settings["directory"]
	case = database	
	
	counter = 0
	
	command = "vol.py -f " + imagename + " --profile=" + imagetype + " " + plugin + " > " + imagename + plugin + ".txt"
	
	Lobotomy.write_to_main_log(database, " Start: " + command)
	Lobotomy.write_to_case_log(casedir, " Start: " + command)
	os.system(command)
	Lobotomy.write_to_main_log(database, " Stop : " + command)
	Lobotomy.write_to_case_log(casedir, " Stop : " + command)


	with open(imagename + plugin + ".txt") as f:
		result = []
		part = []
		#sql = MySQLdb.connect('localhost', 'root', 'ZPRvLVaZReH5BbNJGCu7OeEO1edBaJzh', memdump)
		linePointer = 0
		lastLinePointer = 0
		pointers = []

		for line in f:
			if counter == 1:
				for x in line.split(' '):
					pointers.append(len(x)+1)
				pointers.pop(len(pointers)-1)
				pointers.append(255)
			if counter > 1:
				for x in range(len(pointers)): # Loop aantal kolommen
					item = pointers[x]
					lastLinePointer += item
					part.append(line[linePointer:lastLinePointer].strip('\n').strip(' '))
					linePointer += item
				linePointer = 0
				lastLinePointer = 0
				if DEBUG:
					pass
				result.append(part)
			counter += 1
			part = []

		Lobotomy.write_to_case_log(casedir,"Database: " + database + " Start: running plugin: " + plugin)
		for listitem in result:
			if DEBUG:
				print listitem
			else:
				#cur = sql.cursor()
				sql_line = "INSERT INTO " + plugin + " VALUES ("
				for item in listitem:
					sql_line = sql_line + "'{}',".format(item)
				sql_line = sql_line[:-1] + ")"
				#print sql_line
				#try:
				Lobotomy.exec_sql_query(sql_line, database)

					#cur.execute(sql_line)
					#sql.commit()
				#except MySQLdb.Error, e:
				#	try:
				#		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				#	except IndexError:
				#	   print "MySQL Error: %s" % str(e)
		#sql.close()
		Lobotomy.write_to_case_log(casedir,"Database: " + database + " Stop:  running plugin: " + plugin)

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: multilist.py [Database] [plugin]"
	else:
		main(sys.argv[1], sys.argv[2])

