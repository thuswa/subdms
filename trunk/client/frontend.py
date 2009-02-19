#!/usr/bin/env python
# $Id$
# Last modified Thu Oct  9 23:26:15 2008 on violator
# update count: 79

"""

"""
import os
import pysvn

client = pysvn.Client()

REPONAME="repo"
URR="file://"+os.getcwd()+"/"+REPONAME
doctype=["note","report","list"]
workdir="./workspace"

def createproject(proj):
   """    
   """
   print proj
   #for doc in doctype:
   #   client.mkdir(URR+"/"+proj+"/"+doc,"create doc dirs",1)

def createdocument(docname,doctitle):
   """    
   """
   
   return None

def adddocument(docname,doctitle):
   """    
   """
   return None

def commit(docname,message):
   "commit changes on file"
   client.checkin(work+"/"+docname.replace("-","/"), message)

def checkin(docname,message):
   "check-in file from workspace"
   commit(docname,message) 
   os.remove(work+"/"+docname.replace("-","/"))  ##fix me

   
def checkout(docname):
  "check-out file to workspace"
  client.checkout(URR+docname.replace("-","/"),work)
#  client.lock( 'file.txt', 'reason for locking' )

def release(docname):
   """
   """
   
   return None

###############################################################################
# Helper functions

def __command_output(cmd):
  " Capture a command's standard output. "
  import subprocess
  return subprocess.Popen(
      cmd.split(), stdout=subprocess.PIPE).communicate()[0]

def __grem(path, pattern):
	pattern = re.compile(pattern)
	for each in os.listdir(path):
		if pattern.search(each):
			name = os.path.join(path, each)
			try: os.remove(name)
			except:
				grem(name, '')
				os.rmdir(name)

def __nukedir(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nukedir(path)
        else:
            os.unlink(path)
    os.rmdir(dir)
