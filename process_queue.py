#!/usr/bin/python

import os
import time
import main

Lobotomy = main.Lobotomy()

while True:
    free = True  # Free to do any new task, False if running
    while free:
        data = Lobotomy.read_from_queue()
        if data is not None:
            free = False
            id = data['id']
            command = data['command']
            priority = data['priority']
            print "ID:", id
            print "Command:", command
            print "Priority:", priority
            print "-"*25
            Lobotomy.write_to_main_log('QUEUE PROCESSOR', "Starting running from queue: {}".format(command))
            os.system(command)
            Lobotomy.write_to_main_log('QUEUE PROCESSOR', "Finished running from queue: {}".format(command))
            free = True
    time.sleep(5)