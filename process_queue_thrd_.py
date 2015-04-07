#!/usr/bin/python

import os
import time
import main
import Queue
import threading


Lobotomy = main.Lobotomy()


##############################################################################################################################

def lobthread(data):
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

##############################################################################################################################    


class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        #print "Starting " + self.name
        process_data(self.name, self.q)
        #print "Exiting " + self.name


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()

            print "processing : {}".format(data)
            Lobotomy.write_to_main_log('QUEUE PROCESSOR', "Starting running from queue: {}".format(data))
            os.system(data)
            Lobotomy.write_to_main_log('QUEUE PROCESSOR', "Finished running from queue: {}".format(data))
            print "finished   : {}".format(data)
            print "-"*25
        else:
            queueLock.release()
        time.sleep(3)

if __name__ == "__main__":
    while True:

        threadList = ["Lobotomy Thread-1", "Lobotomy Thread-2", "Lobotomy Thread-3"]
        nameList = ["One", "Two", "Three", "Four", "Five"] # Lijst met opdrachten. **** data = Lobotomy.read_from_queue()
        queueLock = threading.Lock()
        workQueue = Queue.Queue(5)
        threads = []
        threadID = 1
        exitFlag = 0

        # Create new threads
        for tName in threadList:
            thread = myThread(threadID, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadID += 1

        # Fill the queue
        queueLock.acquire()
        for word in nameList:
            try:
                data = Lobotomy.read_from_queue()
                id = data['id']
                command = data['command']
                priority = data['priority']
                free = False

                print "ID:", id
                print "Command:", command
                print "Priority:", priority
                print "-"*25
                workQueue.put(command)
            except:
                print "Nothing to do"
                time.sleep(2)
        queueLock.release()

        # Wait for queue to empty
        while not workQueue.empty():
            pass

        # Notify threads it's time to exit
        exitFlag = 1

        # Wait for all threads to complete
        for t in threads:
            t.join()
        #print "Exiting Main Thread"
