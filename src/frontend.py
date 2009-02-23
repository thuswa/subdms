#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 23:12:16 2009 on violator
# update count: 104
# -*- coding:  utf-8 -*-

import os
import pysvn
import config

"""

"""

client = pysvn.Client()
conf = config.dmsconfig()

def createproject(proj):
   """    
   """
   print proj
   for doc in conf.doctypes:
      client.mkdir(conf.repourl+"/"+proj+"/"+doc, \
                   "create directory for project: "+proj,1)

def createdocument(docname, doctitle):
   """create document"""
   docname.spl
   client.checkout(conf.repourl+'/'+docname.replace("-","/"),conf.workpath)
   return None

def adddocument(docname,doctitle):
   """    
   """
   return None

def commit(docname,message):
   """commit changes on file"""
   client.checkin(conf.workpath+"/"+docname.replace("-","/"), message)

def checkin(docname,message):
   """check-in file from workspace"""
   commit(docname,message) 
   os.remove(conf.workpath+"/"+docname.replace("-","/"))  ##fix me

def checkout(docname):
  """check-out file to workspace"""
  client.checkout(conf.repourl+'/'+docname.replace("-","/"),conf.workpath)
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
