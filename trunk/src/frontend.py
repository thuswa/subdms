#!/usr/bin/env python
# $Id$
# Last modified Fri Feb 27 13:39:23 2009 on havoc
# update count: 192
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil
import string

import config

"""

"""

client = pysvn.Client()
conf = config.dmsconfig()

def createproject(proj):
   """Create a project"""
   print proj
   for doc in conf.doctypes:
      client.mkdir(os.path.join(conf.repourl, proj, doc), \
                   "create directory for project: "+proj,1)

def createdocument(docnamelist, doctitle):
   """
   Create a document
   
   docnamelist: list containing the building blocks of the document name
   doctitle: document title string.
   """
   adddocument(docnamelist, doctitle, conf.tmpltxt)

def adddocument(docnamelist, doctitle, addfile):
   """    
   Add a document
   
   docnamelist: list containing the building blocks of the document name
   doctitle: document title string.
   addfile: path to the file to be added.
   """
   docname=__const_docname(docnamelist)
   docurl=__const_docurl(docnamelist)
   checkoutpath=__const_checkoutpath(docnamelist)
   docpath=__const_docpath(docnamelist)

   # Create doc url in repository and check it out to workspace
   client.mkdir(docurl, "create directory for : "+docname,1)
   client.checkout(docurl, checkoutpath)

   # Copy file to works
   shutil.copyfile(addfile, docpath)
   client.add(docpath)

   # Set document title and commit document
   client.propset('title', doctitle, docpath)
   client.propset('issue', '1', docpath)
   client.propset('status', 'preliminary', docpath)
   client.checkin(docpath, "adding document: "+docname)

   # Remove file from workspace
   shutil.rmtree(checkoutpath)
   
def commit(docnamelist, message):
   """commit changes on file"""
   client.checkin(__const_docpath(docnamelist, message)

def checkin(docnamelist, message):
   """check-in file from workspace"""
   commit(docnamelist, message) 

   # Remove file from workspace
   shutil.rmtree(__const_checkoutpath(docnamelist))

def checkout(docnamelist):
  """check-out file to workspace"""
  client.checkout(__const_docurl(docnamelist), \
                     __const_checkoutpath(docnamelist))
#  client.lock( 'file.txt', 'reason for locking' )

def release(docnamelist):
   """ Release the document"""
   return None

###############################################################################
# Helper functions
def __const_checkoutpath(docnamelist):
   return os.path.join(conf.workpath, \
                          os.path.splitext(__cons_docname(docnamelist))[0])

def __const_docname(docnamelist):
   """ Construct the document file name. """
   return string.join(docnamelist[:-1],'-')+'.'+docnamelist[-1:].pop()

def __const_docurl(docnamelist):
   """ Construct the document url. """
   conslist=[conf.repourl]
   conslist.extend(docnamelist)
   return string.join(conslist[:-1], '/')

def __const_docpath(docnamelist):
   """ Construct the path to the checked out document. """
   return os.path.join(checkoutpath, __const_docname(docnamelist))

def __command_output(cmd):
  """ Capture a command's standard output. """
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
