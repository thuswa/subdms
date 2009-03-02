#!/usr/bin/env python
# $Id$
# Last modified Mon Mar  2 14:06:48 2009 on havoc
# update count: 351
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

def createrepo():
   """ create repsitory and layout """
   subprocess.call(['svnadmin','create',conf.repopath])
   client.mkdir(conf.trunkurl, "create trunk directory",1)
   client.mkdir(conf.tagsurl, "create trunk directory",1)
   client.mkdir(conf.tmplurl, "create templates directory",1)

def installhooks():
   """ Install hooks in repository """
   revhook='pre-revprop-change'
   revhookpath=os.path.join(conf.hookspath, revhook)
   
   # Copy hooks to dir in repository and set to executable
   shutil.copyfile(os.path.abspath(revhook), revhookpath)
   os.chmod(revhookpath,0755)
   
def installtemplates():
   """ Install templates in repository """
   tmplpath=os.path.join(conf.workpath,'templates')
   txtfilepath=os.path.join(tmplpath, conf.tmpltxt.split('/')[1]) #fixme
   
   # Check out templates dir
   client.checkout(conf.tmplurl, tmplpath)
   
   # Add templates to dir
   shutil.copyfile(os.path.abspath(conf.tmpltxt), txtfilepath)
   client.add(txtfilepath)

   # Commit templates
   client.checkin(tmplpath, "installing templates")
   
   # Remove template dir from workspace
   shutil.rmtree(tmplpath)
   
def createproject(proj):
   """Create a project"""
   for doc in conf.doctypes:
      client.mkdir(os.path.join(conf.trunkurl, proj, doc), \
                   "create directory for project: "+proj,1)

def createdocument(docnamelist, doctitle):
   """
   Create a document
   
   docnamelist: list containing the building blocks of the document name
   doctitle: document title string.
   """
   txtfileurl=os.path.join(conf.tmplurl, conf.tmpltxt.split('/')[1]) #fixme
   docname=__const_docname(docnamelist)
   docurl=__const_docurl(docnamelist)
   docfileurl=__const_docfileurl(docnamelist)
   
   # Create document url in repository 
   client.mkdir(docurl, "create directory for : "+docname,1)

   # Create document from template
   server_side_copy(txtfileurl, docfileurl, "Create document: "+docname)

   # Set document title and commit document
   client.propset('title', doctitle, docfileurl)
   client.propset('issue', '1', docfileurl)
   client.propset('status', 'preliminary', docfileurl)

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
   client.checkin(docpath, "Add document: "+docname)

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
   issue_no=str(getissueno)
   docname=__const_docname(docnamelist)

   # Set status of document to released
   client.propset('status', 'released', __const_docurl(docnamelist))

   # Create tag
   server_side_copy(__const_docurl(docnamelist), \
                    __const_doctagurl(docnamelist, issue_no), \
                    "Release "+docname+", issue "+issue_no)

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

def server_side_copy(source, target, log_message):
   """ Server side copy in repository URL -> URL """
   def get_log_message():
      return True, log_message
   client.callback_get_log_message = get_log_message
   client.copy(source, target)

def server_side_propset(propname, propvalue, fileurl):
   """ Workaround for setting properties in repo via URL """ 
   subprocess.call(['svn','propset',conf.repopath])

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
   docurllist=[conf.trunkurl]
   docurllist.extend(docnamelist[:-1])
   return string.join(docurllist, '/')

def __const_docfileurl(docnamelist):
   """ Construct the document file url. """
   return string.join([__const_docurl(docnamelist), \
                       __const_docname(docnamelist)], '/')

def __const_doctagurl(docnamelist, issue_no):
   """ Construct the document tag url. """
   docurllist=[conf.tagsurl]
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
