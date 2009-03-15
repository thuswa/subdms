#!/usr/bin/env python
# $Id$
# Last modified Sun Mar 15 20:22:49 2009 on violator
# update count: 464
# -*- coding:  utf-8 -*-
#
# subdms - A document management system based on subversion.
# Copyright (C) 2009  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pysvn
import shutil

import database
import lowlevel

"""

"""

client = pysvn.Client()
conf = lowlevel.config()
docs = lowlevel.docname()
db = database.sqlitedb()

def createproject(proj):
   """Create a project"""
   for doc in conf.doctypes:
      client.mkdir(os.path.join(conf.trunkurl, proj, doc), \
                   conf.newproj+" create directory for project: "+proj,1)

def createdocument(docnamelist, doctitle):
   """
   Create a document
   
   docnamelist: list containing the building blocks of the document name
   doctitle: document title string.
   """
   txtfileurl=os.path.join(conf.tmplurl, conf.tmpltxt) #fixme
   docname=docs.const_docfname(docnamelist)
   docurl=docs.const_docurl(docnamelist)
   docfileurl=docs.const_docfileurl(docnamelist)
   checkoutpath=docs.const_checkoutpath(docnamelist)
   docpath=docs.const_docpath(docnamelist)
   
   # Create document url in repository
   client.mkdir(docurl, "create directory for : "+docname,1)

   # Create document from template
   server_side_copy(txtfileurl, docfileurl, "Create document: "+docname)
   client.checkout(docurl, checkoutpath)
   
   # Set document title and commit document
   client.propset(conf.proplist[0], doctitle, docpath)
   client.propset(conf.proplist[1], '1', docpath)
   client.propset(conf.proplist[2], conf.statuslist[0], docpath)
   client.checkin(docpath, conf.newdoc+ \
                  " commit document properties for: "+docname)
   
def adddocument(docnamelist, doctitle, addfile):
   """    
   Add a document
   
   docnamelist: list containing the building blocks of the document name
   doctitle: document title string.
   addfile: path to the file to be added.
   """
   docname=docs.const_docfname(docnamelist)
   docurl=docs.const_docurl(docnamelist)
   checkoutpath=docs.const_checkoutpath(docnamelist)
   docpath=docs.const_docpath(docnamelist)

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

def commit(docnamelist, message):
   """commit changes on file"""
   client.checkin(docs.const_docpath(docnamelist, message))

def checkin(docnamelist, message):
   """check-in file from workspace"""
   commit(docnamelist, message) 

   # Remove file from workspace
   shutil.rmtree(docs.const_checkoutpath(docnamelist))

def checkout(docnamelist):
  """check-out file to workspace"""
  client.checkout(docs.const_docurl(docnamelist), \
                     docs.const_checkoutpath(docnamelist))
#  client.lock( 'file.txt', 'reason for locking' )

def release(docnamelist):
   """Release the document"""
   issue_no=str(getissueno)
   docname=docs.const_docfname(docnamelist)
   newissuepath=docs.const_doctagurl(docnamelist, issue_no)

   # Set status of document to released
   client.propset(conf.proplist[2], conf.statuslist[4], \
                  docs.const_docpath(docnamelist))
   checkin(docnamelist, "Set status to released on "+docname)
   
   # Create tag
   server_side_copy(docs.const_docurl(docnamelist), \
                    docs.const_doctagurl(docnamelist, issue_no), \
                    " Release "+docname+", issue "+issue_no)

   # Set previous issue to obsolete
   if issueno > 1:
      oldissue=issue_no - 1
      oldissuepath=docs.const_doctagurl(docnamelist, oldissue)
      client.checkout(oldissuepath, docs.const_checkoutpath(docnamelist))
      client.propset('status', 'obsolete', docs.const_docpath(docnamelist))
      checkin(docnamelist, "Set status to obsolete on " \
              +docname+" issue "+oldissue)
      
def newissue(docnamelist):
   """Create new issue of the document"""
   new_issue_no = str(getissueno + 1)
   client.propset('status', 'preliminary', docs.const_docurl(docnamelist))
   client.propset('issue', new_issue_no,  docs.const_docurl(docnamelist))
   
def getissueno(docnamelist):
   """ Get document issue number """ 
   return int(client.propget('issue', \
                             docs.const_docurl(docnamelist)).values().pop())

def gettitle(docnamelist):
   """ Get document title """ 
   return client.propget('title', docs.const_docurl(docnamelist)).values().pop()

def getstatus(docnamelist):
   """ Get document status """ 
   return client.propget('status', docs.const_docurl(docnamelist)).values().pop()

def server_side_copy(source, target, log_message):
   """ Server side copy in repository URL -> URL """
   def get_log_message():
      return True, log_message
   client.callback_get_log_message = get_log_message
   client.copy(source, target)

def createdocnamelist(project, doctype, docext):
   """
   Create docnamelist - list containing the building blocks of
   the document name
   """
   docno="%04d" % (db.getdocno(project, doctype) + 1)
   return [project, doctype, docno, docext]

def ischeckedout(docnamelist):
   """ Return true if docname is checked out. """
   return None

def reverttohead(docnamelist):
   """ Revert to head revision undo local changes. """
   return None

def reverttoprerev(docnamelist):
   """ Revert to previous revision. """
   return None

