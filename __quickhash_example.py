# source: http://python-forensics.org/wp-content/uploads/2014/03/QHash.txt

#
# Forensic Utility
# Python Quick Hash Utility
#
# Command line operation
# QHash
#
#
# Produced by Python-Forensics.org
# Produced for the greater forensic community
# Free to use, modify and distribute
# NO HASP REQUIRED
#
# import the libraries that we will use
import os, os.path, stat, time
import sys
import hashlib
from datetime import date, timedelta

# Constant Representing the a Buffer Size to Read
# You can change this value if you like to be larger chunks
# say 1024000000 would be ONE_GB that should also work on most
# modern systems

ONE_MB = 1024000  # 1 MB


# dirsNotUsed = []
 
#
# processDirectories
# parameters StartingPath
#
# Process is to walk through the directory and all subdirectories
# and for each file encountered perform
 
def processDirectories(theDir, useHash):
 
    global ProcessCount
    global ErrorCount
 
    ProcessCount = 0
    ErrorCount = 0
 
    for root, dirs, files in os.walk(theDir):
 
        for file in files:
            fname = os.path.join(root, file)
            result = hashFile(fname, file, useHash)
            if result is True:
                ProcessCount += 1
            else:
                ErrorCount += 1
 
def hashFile(theFile, simpleName, useHash):
 
    # Verify that the path is valid
    if os.path.exists(theFile):
     
        #Verify that the path is not a symbolic link
        if not os.path.islink(theFile):
         
            #Verify that the file is real
            if os.path.isfile(theFile):
             
                try:
                    #Attempt to open the file
                    f = open(theFile, 'rb')
                except IOError:
                    #if open fails report the error
                    print "\nOpen Failed " + theFile + "\n"
                    return
                
                try:
                    
                    if useHash == 'MD5':
                        hash=hashlib.md5()
                    elif useHash == 'SHA1':
                        hash=hashlib.sha1()
                    elif useHash == 'SHA256':
                        hash=hashlib.sha256()
                    elif useHash == 'SHA384':
                        hash=hashlib.sha384()
                    elif useHash == 'SHA512':
                        hash=hashlib.sha512()
                        
                    # Attempt to read the file and hash the contents

                    rdBuffer = 'ok'
                    
                    while len(rdBuffer):
                        rdBuffer = f.read(ONE_MB)   
                        hash.update(rdBuffer)
                        
                    #File processing completed
                    #Close the Active File
                    f.close()

                    # Once complete obtain the hex digest
                    hexOfHash = hash.hexdigest().upper()

                except IOError:
                    # if read fails, then close the file and report error
                    f.close()
                    print "\nFile Read Error " + theFile +" \n"
                    return

                #lets query the file stats

                theFileStats =  os.stat(theFile)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(theFile)
             
                #Print the simple file name
                print "File : " + theFile
             
                # print the size of the file in Bytes
                print "Size : %s bytes" % str(size)
             
                #print the File Hash
                print hashType+': '+ hexOfHash
                
                #print MAC Times
                print "Last Modified : %s" % time.ctime(mtime)
                print "Last Access   : %s" % time.ctime(atime)
                print "Created Time  : %s" % time.ctime(ctime)
                  
                print "================================\n"
                 
                return True
 
            else:
                print '[' + repr(simpleName) + ", Skipped Not a File" + ']'          
                return False
        else:
            print '[' + repr(simpleName) + ", Skipped Link Not a File" + ']'
            return False
    else:
        return False
 
 
if __name__ == '__main__':
 
    # Collect User Input:
    
    print 'Welcome to the Python Quick Hash Utility V 1.2'
    print

    investigatorName = raw_input('Investigator Name: ')
    organizationName = raw_input('Organization Name: ')
    caseNumber = raw_input('Case Number: ')
    
    hashValue = raw_input('Hash Type: 0=MD5 1=SHA1 2=SHA256 3=SHA384 4=SHA512: ')
    if hashValue.isdigit():
        if int(hashValue) in range(0, 5):
            if hashValue == '0':
                hashType = 'MD5'
            elif hashValue == '1':
                hashType = 'SHA1'
            elif hashValue == '2':
                hashType = 'SHA256'
            elif hashValue == '3':
                hashType = 'SHA384'
            elif hashValue == '4':
                hashType = 'SHA512'          
    else:
        print 'Invalid Hash Type'
        sys.exit()
        
    
    thePath = raw_input('Path: ')
    if not os.path.isdir(thePath):
        print 'Invalid Path Name'
        sys.exit()
        
    print
    print 'Specify Output Filename, or simply Press Enter to Display Results to the Screen'
    resultsFile = raw_input('Result File: ')
    
    if resultsFile:  # If result file name not empty, then attempt to redirect standard output
        try:
            sys.stdout = open(resultsFile, 'w')
        except:
            print 'Invalid Result File Name'
            sys.exit() 
    
    #get local time for the report
    
    localtime = time.asctime( time.localtime(time.time()) )
 
    start = time.time()
    
    print
    print '========================================================='
    print 'Starting Quick Hash V 1.2, Ptyhon-Forensics.org'
    print
    
    print 'Investigator: '+ investigatorName
    print 'Organization: '+ organizationName
    print 'Case Number : '+ caseNumber
    print 'Hash Type   : '+ hashType
    print 'Start Path  : '+ thePath
    print 'System Type : '+ sys.platform
    print 'Version     : '+ sys.version
    print
    
    print "Start Time  : %s" % localtime
    
    if resultsFile:
        print 'Output Selected: ' + resultsFile
    else:
        print 'Output Selected: Main Display'
        
    print
    print '===================================='
    
     
    #Perform Hashing on specified Directory
    #The only argument is the path to start the scan
 
    processDirectories(thePath, hashType)
 
    #Once completed save the ending time
 
    end = time.time()
 
    #Calculate the duration of the scan

    duration = end - start
 
    #Print out the Files Processed, Error Count and Duration

    print("\nFiles Processed: " + str(ProcessCount) + "\tin " + str(duration) + " seconds")
    print("Error Count: " + str(ErrorCount))

    sys.stdout = sys.__stdout__
    
    print("Hashing Completed" + '\n')
    