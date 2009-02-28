#!/usr/bin/env python
# $Id$
# Last modified Sat Feb 28 11:45:04 2009 on violator
# update count: 249
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

def createrepolayout():
   """Create repository layout"""
   client.mkdir(os.path.join(conf.repourl, 'trunk'), "create trunk directory",1)
   client.mkdir(os.path.join(conf.repourl, 'tags'), "create trunk directory",1)
   client.mkdir(os.path.join(conf.repourl, 'templates'), \
                "create templates directory",1)

def installtemplates():
   """ Install templates in repository """
   return NONE
   
   
def createproject(proj):
   """Create a project"""
   print proj
   for doc in conf.doctypes:
      client.mkdir(os.path.join(conf.repourl, 'trunk', proj, doc), \
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

   # Create document url in repository and check it out to workspace
   client.mkdir(docurl, "create directory for : "+docname,1)
   client.checkout(docurl, checkoutpath)

   # Copy file to workspace
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
   client.checkin(__const_docpath(docnamelist, message))

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
   """Release the document"""
   issue_no = str(getissueno)
   client.propset('status', 'released', __const_docurl(docnamelist))
   client.copy(__const_docurl(docnamelist), \
               __const_doctagurl(docnamelist, issue_no))

def newissue(docnamelist):
   """Create new issue of the document"""
   new_issue_no = str(getissueno + 1)
   client.propset('status', 'preliminary', __const_docurl(docnamelist))
   client.propset('issue', new_issue_no,  __const_docurl(docnamelist))
   
def getissueno(docnamelist):
   """ Get document issue number """ 
   return int(client.propget('issue', \
                             __const_docurl(docnamelist)).values().pop())

def gettitle(docnamelist):
   """ Get document title """ 
   return client.propget('title', __const_docurl(docnamelist)).values().pop()

def getstatus(docnamelist):
   """ Get document status """ 
   return client.propget('status', __const_docurl(docnamelist)).values().pop()


###############################################################################
# Helper functions
def __const_checkoutpath(docnamelist):
   """ Construct the check-out path """
   return os.path.join(conf.workpath, \
                          os.path.splitext(__const_docname(docnamelist))[0])

def __const_docname(docnamelist):
   """ Construct the document file name. """
   return string.join(docnamelist[:-1],'-')+'.'+docnamelist[-1:].pop()

def __const_docurl(docnamelist):
   """ Construct the document url. """
   docurllist=[conf.repourl]
   docurllist.extend('trunk')
   docurllist.extend(docnamelist[:-1])
   return string.join(docurllist, '/')

def __const_doctagurl(docnamelist, issue_no):
   """ Construct the document tag url. """
   docurllist=[conf.repourl]
   docurllist.extend('tags')
   docurllist.extend(docnamelist[:-1])
   docurllist.extend(issueno)
   return string.join(docurllist, '/')


def __const_docpath(docnamelist):
   """ Construct the path to the checked out document. """
   return os.path.join(__const_checkoutpath(docnamelist), \
                       __const_docname(docnamelist))

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
