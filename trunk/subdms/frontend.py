#!/usr/bin/env python
# $Id$
# Last modified Wed Apr  8 16:46:25 2009 on violator
# update count: 865
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

import lowlevel

""" Frontend classes """

class project:
   def __init__(self):
      """ Initialize project class """
      self.client = pysvn.Client()
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()
      
   def createproject(self, project):
      """ Create project method. """
      for doc in self.conf.doctypes:
         self.client.mkdir(self.link.const_doctypeurl(project, doc), \
                           self.conf.newproj+"Create directory for project: "\
                           +project,1)
         
################################################################################

class document:
   def __init__(self):
      """ Initialize project class """
      self.client = pysvn.Client()
      self.cmd = lowlevel.command()
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()
      self.status = docstatus()

   def createdocument(self, createfromurl, docnamelist, doctitle):
      """
      Create a document

      createfromurl: link in repository to the template or document that
                     this new document should be based on.
      docnamelist: list containing the building blocks of the document name
      doctitle: document title string.
      """
      docname=self.link.const_docfname(docnamelist)
      docurl=self.link.const_docurl(docnamelist)
      docfileurl=self.link.const_docfileurl(docnamelist)
      checkoutpath=self.link.const_checkoutpath(docnamelist)
      docpath=self.link.const_docpath(docnamelist)

      # Create document url in repository
      self.client.mkdir(docurl, "create directory for : "+docname,1)
      
      # Create document from template or existing document
      self.server_side_copy(createfromurl, docfileurl, "Create document: "\
                            +docname)
      self.client.checkout(docurl, checkoutpath)
      
      # Set document title and commit document
      self.settitle(doctitle, docpath)
      self.status.setpreliminary(docpath)

      #self.client.propset(conf.proplist[2], conf.svnkeywords, docpath) 
      self.client.checkin(docpath, self.conf.newdoc+ \
                     "Commit document properties for: "+docname)
   
   def adddocument(self, addfilepath, docnamelist, doctitle):
      """    
      Add an existing document 

      addfilepath: path to the file to be added.
      docnamelist: list containing the building blocks of the document name
      doctitle: document title string.
      """
      docname=self.link.const_docfname(docnamelist)
      docurl=self.link.const_docurl(docnamelist)
      docfileurl=self.link.const_docfileurl(docnamelist)
      checkoutpath=self.link.const_checkoutpath(docnamelist)
      docpath=self.link.const_docpath(docnamelist)

      # Create document url in repository and check it out to workspace
      self.client.mkdir(docurl, "create directory for : "+docname,1)
      self.client.checkout(docurl, checkoutpath)
      
      # Copy file to workspace
      self.cmd.copyfile(addfilepath, docpath)
      self.client.add(docpath)

      # Set document title and commit document
      self.settitle(doctitle, docpath)
      self.status.setpreliminary(docpath)
      self.setsvnkeywords(docpath)

      self.client.checkin(docpath, self.conf.newdoc+ \
                     "Commit document properties for: "+docname)

   def commit(self, docnamelist, message):
      """commit changes on file"""
      self.client.checkin(self.link.const_docpath(docnamelist), message)

   def checkin(self, docnamelist):
      """check-in file from workspace"""
      docname = self.link.const_docname(docnamelist)
      message = "Checking in: "+docname
      self.commit(docnamelist, message) 
      # Remove file from workspace
      self.cmd.rmtree(self.link.const_checkoutpath(docnamelist))
      return message
      
   def checkout(self, docnamelist):
      """check-out file to workspace"""

      # Check status of doucument 
      if self.status.isreleased(docnamelist) or \
         self.status.isobsolete(docnamelist):
         self.client.export(self.link.const_docurl(docnamelist), \
                       self.link.const_checkoutpath(docnamelist))
         self.cmd.setreadonly(self.link.const_docpath(docnamelist))
      else:                  
         self.client.checkout(self.link.const_docurl(docnamelist), \
                         self.link.const_checkoutpath(docnamelist))
      #  self.client.lock( 'file.txt', 'reason for locking' )

   def release(self, docnamelist):
      """Release the document"""
      current_issue = self.getissueno(docnamelist)
      docname = self.link.const_docname(docnamelist)
      message = "Release "+docname

      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)

      # Set status of document to released
      self.status.setreleased(self.link.const_docpath(docnamelist))
      self.commit(docnamelist, self.conf.release+message)

      # Remove file from workspace
      self.cmd.rmtree(self.link.const_checkoutpath(docnamelist))
      
      # Set previous issue to obsolete
      if current_issue > 1:
         old_issue = str(current_issue - 1)
         old_docnamelist = self.setissueno(docnamelist, old_issue)
         old_docname = self.link.const_docname(old_docnamelist)
         old_docpath = self.link.const_docpath(old_docnamelist)
         old_docurl = self.link.const_docurl(old_docnamelist)
         self.client.checkout(old_docurl, \
                         self.link.const_checkoutpath(old_docnamelist))
         self.status.setobsolete(old_docpath)
         self.commit(old_docnamelist, \
                     self.conf.obsolete+"Set status to obsolete on " \
                     +old_docname)
         # Remove file from workspace
         self.cmd.rmtree(self.link.const_checkoutpath(old_docnamelist))
      return message

   def editdocument(self, docnamelist):
      """ Edit the document. """
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
      self.cmd.launch_editor(docnamelist)   
      
   def newissue(self, docnamelist):
      """Create new issue of the document"""
      new_issue = str(self.getissueno(docnamelist) + 1)
      new_docnamelist = self.setissueno(docnamelist, new_issue)
      docname = self.link.const_docname(new_docnamelist)
      docurl=self.link.const_docurl(new_docnamelist)
      docfileurl=self.link.const_docfileurl(new_docnamelist)
      docpath = self.link.const_docpath(new_docnamelist)
      checkoutpath=self.link.const_checkoutpath(new_docnamelist)
      message = " Created "+docname

      # Create document url in repository
      self.client.mkdir(docurl, "create directory for : "+docname,1)

      # Copy issue to new issue
      self.server_side_copy(self.link.const_docfileurl(docnamelist), \
                            docfileurl, message)
      self.client.checkout(docurl, checkoutpath)
      
      # Set document title and commit document
      self.status.setpreliminary(docpath)
      self.client.checkin(docpath, self.conf.newdoc+ \
                     "Commit document properties for: "+docname)
      return message   
         
   def getissueno(self, docnamelist):
      """ Get document issue number. """ 
      return int(docnamelist[3])

   def setissueno(self, docnamelist, issue_no):
      """ Set document issue number. """ 
      returnlist = docnamelist[:3]
      returnlist.extend([issue_no, docnamelist[4]])
      return returnlist

   def gettitle(self, docnamelist):
      """ Get document title. """ 
      return self.client.propget('title', \
                  self.link.const_docurl(docnamelist)).values().pop()

   def settitle(self, doctitle, docpath):
      """ Set document title. """ 
      self.client.propset(self.conf.proplist[0], doctitle, docpath)

   def setsvnkeywords(self, docpath):
      """ Set svn keywords. """  
      self.client.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                          docpath) 

   def ischeckedout(self, docnamelist):
      """ Return true if docname is checked out. """
      if os.path.exists(os.path.join(\
         self.link.const_checkoutpath(docnamelist), '.svn')):
         return True
      else:
         return False

   def getstate(self, docnamelist):
      """ Get document state. """
      if self.ischeckedout(docnamelist):
         docpath = self.link.const_docpath(docnamelist)
         state = self.client.status(docpath)[0]
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
      self.client.callback_get_log_message = get_log_message
      self.client.copy(source, target)

   def reverttohead(self, docnamelist):
      """ Revert to head revision undo local changes. """
      return None
   
   def reverttoprerev(self, docnamelist):
      """ Revert to previous revision. """
      return None

################################################################################

class docstatus:
   def __init__(self):
      """ Initialize document status class """
      self.client = pysvn.Client()
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()

   def getstatus(self, docnamelist):
      """ Get document status """ 
      return self.client.propget('status', \
                            self.link.const_docurl(docnamelist)).values().pop()

   def setpreliminary(self, docpath):
      """ Set document status to preliminary. """ 
      self.client.propset(self.conf.proplist[1], \
                          self.conf.statuslist[0], docpath)

   def setreleased(self, docpath):
      """ Set document status to released. """ 
      self.client.propset(self.conf.proplist[1], self.conf.statuslist[4], \
                          docpath)

   def setobsolete(self, docpath):
      """ Set document status to obsolete. """
      self.client.propset(self.conf.proplist[1], self.conf.statuslist[5], \
                          docpath)


   def ispreliminary(self, docnamelist):
      """ Return true if document is released. """
      if getstatus(self, docnamelist) == self.conf.statuslist[0]:
         return True
      else:
         return False

   def isreleased(self, docnamelist):
      """ Return true if document is released. """
      if getstatus(self, docnamelist) == self.conf.statuslist[5]:
         return True
      else:
         return False

   def isobsolete(self, docnamelist):
      """ Return true if document is obsolete. """
      if getstatus(self, docnamelist) == self.conf.statuslist[5]:
         return True
      else:
         return False
