#!/usr/bin/env python
# $Id$
# Last modified Wed Apr  1 22:47:58 2009 on violator
# update count: 748
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

""" Frontend classes """

client = pysvn.Client()
cmd = lowlevel.command()
conf = lowlevel.config()
docs = lowlevel.docname()
db = database.sqlitedb()

class project:
   def createproject(self, projname):
      """Create a project"""
      for doc in conf.doctypes:
         client.mkdir(os.path.join(conf.trunkurl, projname, doc), \
                      conf.newproj+"Create directory for project: "+projname,1)

class document:
   def createdocument(self, createfromurl, docnamelist, doctitle):
      """
      Create a document

      createfromurl: link in repository to the template or document that
                     this new document should be based on.
      docnamelist: list containing the building blocks of the document name
      doctitle: document title string.
      """
      docname=docs.const_docfname(docnamelist)
      docurl=docs.const_docurl(docnamelist)
      docfileurl=docs.const_docfileurl(docnamelist)
      checkoutpath=docs.const_checkoutpath(docnamelist)
      docpath=docs.const_docpath(docnamelist)

      # Create document url in repository
      client.mkdir(docurl, "create directory for : "+docname,1)
      
      # Create document from template or existing document
      self.server_side_copy(createfromurl, docfileurl, "Create document: "\
                            +docname)
      client.checkout(docurl, checkoutpath)
      
      # Set document title and commit document
      client.propset(conf.proplist[0], doctitle, docpath)
      client.propset(conf.proplist[1], conf.statuslist[0], docpath)
      #client.propset(conf.proplist[2], conf.svnkeywords, docpath) 
      client.checkin(docpath, conf.newdoc+ \
                     "Commit document properties for: "+docname)
   
   def adddocument(self, addfilepath, docnamelist, doctitle):
      """    
      Add an existing document 

      addfilepath: path to the file to be added.
      docnamelist: list containing the building blocks of the document name
      doctitle: document title string.
      """
      docname=docs.const_docfname(docnamelist)
      docurl=docs.const_docurl(docnamelist)
      docfileurl=docs.const_docfileurl(docnamelist)
      checkoutpath=docs.const_checkoutpath(docnamelist)
      docpath=docs.const_docpath(docnamelist)

      # Create document url in repository and check it out to workspace
      client.mkdir(docurl, "create directory for : "+docname,1)
      client.checkout(docurl, checkoutpath)
      
      # Copy file to workspace
      shutil.copyfile(addfilepath, docpath)
      client.add(docpath)
      print docpath
      # Set document title and commit document
      client.propset(conf.proplist[0], doctitle, docpath)
      client.propset(conf.proplist[1], conf.statuslist[0], docpath)
      client.propset(conf.proplist[2], conf.svnkeywords, docpath) 
      client.checkin(docpath, conf.newdoc+ \
                     "Commit document properties for: "+docname)

   def commit(self, docnamelist, message):
      """commit changes on file"""
      client.checkin(docs.const_docpath(docnamelist), message)

   def checkin(self, docnamelist):
      """check-in file from workspace"""
      docname = docs.const_docname(docnamelist)
      message = "Checking in: "+docname
      self.commit(docnamelist, message) 
      # Remove file from workspace
      shutil.rmtree(docs.const_checkoutpath(docnamelist))
      return message
      
   def checkout(self, docnamelist):
      """check-out file to workspace"""

      # Check status of doucument 
      if self.getstatus(docnamelist) == conf.statuslist[5] or \
         self.getstatus(docnamelist) == conf.statuslist[4]:
         client.export(docs.const_docurl(docnamelist), \
                       docs.const_checkoutpath(docnamelist))
         # Set file to read-only
         os.chmod(docs.const_docpath(docnamelist), 0444)
      else:                  
         client.checkout(docs.const_docurl(docnamelist), \
                         docs.const_checkoutpath(docnamelist))
      #  client.lock( 'file.txt', 'reason for locking' )

   def release(self, docnamelist):
      """Release the document"""
      current_issue = self.getissueno(docnamelist)
      docname = docs.const_docname(docnamelist)
      message = "Release "+docname

      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)

      # Set status of document to released
      client.propset(conf.proplist[1], conf.statuslist[4], \
                     docs.const_docpath(docnamelist))
      self.commit(docnamelist, conf.release+message)

      # Remove file from workspace
      shutil.rmtree(docs.const_checkoutpath(docnamelist))
      
      # Set previous issue to obsolete
      if current_issue > 1:
         old_issue = str(current_issue - 1)
         old_docnamelist = self.setissueno(docnamelist, old_issue)
         old_docname = docs.const_docname(old_docnamelist)
         old_docpath = docs.const_docpath(old_docnamelist)
         old_docurl = docs.const_docurl(old_docnamelist)
         client.checkout(old_docurl, \
                         docs.const_checkoutpath(old_docnamelist))
         client.propset(conf.proplist[1], conf.statuslist[5], old_docpath)
         self.commit(old_docnamelist, \
                      conf.obsolete+"Set status to obsolete on "+old_docname)
         # Remove file from workspace
         shutil.rmtree(docs.const_checkoutpath(old_docnamelist))
      return message

   def editdocument(self, docnamelist):
      """ Edit the document. """
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
      cmd.launch_editor(docs.const_docpath(docnamelist))   
      
   def newissue(self, docnamelist):
      """Create new issue of the document"""
      new_issue = str(self.getissueno(docnamelist) + 1)
      new_docnamelist = self.setissueno(docnamelist, new_issue)
      docname = docs.const_docname(new_docnamelist)
      docurl=docs.const_docurl(new_docnamelist)
      docfileurl=docs.const_docfileurl(new_docnamelist)
      docpath = docs.const_docpath(new_docnamelist)
      checkoutpath=docs.const_checkoutpath(new_docnamelist)
      message = " Created "+docname

      # Create document url in repository
      client.mkdir(docurl, "create directory for : "+docname,1)

      # Copy issue to new issue
      self.server_side_copy(docs.const_docfileurl(docnamelist), \
                            docfileurl, message)
      client.checkout(docurl, checkoutpath)
      
      # Set document title and commit document
      client.propset(conf.proplist[1], conf.statuslist[0], docpath)
      client.checkin(docpath, conf.newdoc+ \
                     "Commit document properties for: "+docname)
      return message   
         
   def getissueno(self, docnamelist):
      """ Get document issue number """ 
      return int(docnamelist[3])

   def setissueno(self, docnamelist, issue_no):
      """ Set document issue number """ 
      returnlist = docnamelist[:3]
      returnlist.extend([issue_no, docnamelist[4]])
      return returnlist

   def gettitle(self, docnamelist):
      """ Get document title """ 
      return client.propget('title', \
                            docs.const_docurl(docnamelist)).values().pop()

   def getstatus(self, docnamelist):
      """ Get document status """ 
      return client.propget('status', \
                            docs.const_docurl(docnamelist)).values().pop()

   def createdocnamelist(self, project, doctype, issue, docext):
      """
      Create docnamelist - list containing the building blocks of
      the document name
      """
      docno="%04d" % (db.getdocno(project, doctype) + 1)
      return [project, doctype, docno, issue, docext]

   def ischeckedout(self, docnamelist):
      """ Return true if docname is checked out. """
      if os.path.exists(os.path.join(docs.const_checkoutpath(docnamelist), \
                                     '.svn')):
         return True
      else:
         return False

   def reverttohead(self, docnamelist):
      """ Revert to head revision undo local changes. """
      return None
   
   def reverttoprerev(self, docnamelist):
      """ Revert to previous revision. """
      return None

   def getstate(self, docnamelist):
      """ Get document state. """
      if self.ischeckedout(docnamelist):
         docpath = docs.const_docpath(docnamelist)
         state = client.status(docpath)[0]
         return_state = ['O', 'Checked Out']
         if state.text_status == pysvn.wc_status_kind.modified:
            return_state = ['M', 'Modified']
         if state.text_status == pysvn.wc_status_kind.conflicted:
            return_state = ['C', 'Conflict'] 
      else:
         return_state = ['I', 'Checked In']
      return return_state
   
   def server_side_copy(self, source, target, log_message):
      """ Server side copy in repository URL -> URL """
      def get_log_message():
         return True, log_message
      client.callback_get_log_message = get_log_message
      client.copy(source, target)
