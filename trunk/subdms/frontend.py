#!/usr/bin/env python
# $Id$
# Last modified Thu Apr 23 13:05:51 2009 on violator
# update count: 1045
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

import integration
import lowlevel

""" Front-end classes. """

class project:
   def __init__(self):
      """ Initialize project class """
      self.client = pysvn.Client()
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()

   def createcategory(self, category):
      """ Create category dir in repo. """
      self.client.mkdir(self.link.const_caturl(category), \
                        "Created a category", 1)
      
   def createproject(self, category, project, description, doctypes):
      """ Create project dir in repo. """
      self.client.mkdir(self.link.const_projurl(category, project), \
                        self.conf.newproj+description,1)
      self.adddoctypes(category, project, doctypes)

   def adddoctypes(self, category, project, doctypes):
      """ Add new doctypes. """
      for doc in doctypes:
         self.client.mkdir(self.link.const_doctypeurl(category, project, doc), \
                           self.conf.newdoctype+"Added doctype",1)
      
################################################################################

class document:
   def __init__(self):
      """ Initialize project class """
      self.client = pysvn.Client()
      self.cmd = lowlevel.command()
      self.conf = lowlevel.config()
      self.integ = integration.docinteg()
      self.link = lowlevel.linkname()
      self.status = docstatus()
      self.svncmd = lowlevel.svncmd()

   def createdocument(self, createfromurl, docnamelist, doctitle, dockeywords):
      """
      Create a document

      createfromurl: link in repository to the template or document that
                     this new document should be based on.
      docnamelist: list containing the building blocks of the document name
      doctitle: document title string.
      """
      docurl=self.link.const_docurl(docnamelist)
      docfileurl=self.link.const_docfileurl(docnamelist)
      checkoutpath=self.link.const_checkoutpath(docnamelist)
      docpath=self.link.const_docpath(docnamelist)

      # Create document url in repository
      self.client.mkdir(docurl, "Document directory created.", 1)
      
      # Create document from template or existing document
      self.svncmd.server_side_copy(createfromurl, docfileurl, \
                                   "Document created")
      self.client.checkout(docurl, checkoutpath)

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.setallfields(docnamelist, doctitle, dockeywords, \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document title and commit document
      self.settitle(doctitle, docpath)
      self.setkeywords(dockeywords, docpath)
      self.status.setpreliminary(docpath)

      #self.client.propset(conf.proplist[], conf.svnkeywords, docpath) 
      self.client.checkin(docpath, self.conf.newdoc+ \
                     "Commited document properties")
   
   def adddocument(self, addfilepath, docnamelist, doctitle, dockeywords):
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
      self.client.mkdir(docurl, "Document directory created.", 1)
      self.client.checkout(docurl, checkoutpath)
      
      # Copy file to workspace
      self.cmd.copyfile(addfilepath, docpath)
      self.client.add(docpath)

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.setallfields(docnamelist, doctitle, dockeywords, \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document title and commit document
      self.settitle(doctitle, docpath)
      self.setkeywords(dockeywords, docpath)
      self.setsvnkeywords(docpath)
      self.status.setpreliminary(docpath)

      self.client.checkin(docpath, self.conf.newdoc+ \
                          "Commited document properties.")

   def commit(self, docnamelist, message):
      """ Commit changes on file. """
      self.client.checkin(self.link.const_docpath(docnamelist), message)

   def checkin(self, docnamelist):
      """ Check-in file from workspace. """
      docname = self.link.const_docname(docnamelist)
      message = "Checking in: "+docname
      self.commit(docnamelist, message) 
      # Remove file from workspace
      self.cmd.rmtree(self.link.const_checkoutpath(docnamelist))
      return message
      
   def checkout(self, docnamelist):
      """ Check-out file to workspace. """
      self.client.checkout(self.link.const_docurl(docnamelist), \
                           self.link.const_checkoutpath(docnamelist))
      #  self.client.lock( 'file.txt', 'reason for locking' )

   def export(self, docnamelist):
      """ Export file to workspace. """
      checkoutpath = self.link.const_readonlypath(docnamelist)
      docpath = self.link.const_readonlyfilepath(docnamelist)
#      self.cmd.rmtree(checkoutpath)
      self.client.export(self.link.const_docurl(docnamelist), \
                         checkoutpath, True)
      self.cmd.setreadonly(docpath)

   def release(self, docnamelist):
      """ Release the document. """
      current_issue = self.getissueno(docnamelist)
      docname = self.link.const_docname(docnamelist)
      message = "Release "+docname

      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.releaseupdate(docnamelist)
         
      # Set status of document to released
      self.status.setreleased(self.link.const_docpath(docnamelist))
      self.commit(docnamelist, self.conf.release+"Status set to released")

      # Remove file from workspace
      self.cmd.rmtree(self.link.const_checkoutpath(docnamelist))
      
      # Set previous issue to obsolete
      if current_issue > 1:
         old_issue = str(current_issue - 1)
         old_docnamelist = self.setissueno(docnamelist, old_issue)
         old_docpath = self.link.const_docpath(old_docnamelist)
         old_docurl = self.link.const_docurl(old_docnamelist)
         self.client.checkout(old_docurl, \
                         self.link.const_checkoutpath(old_docnamelist))
         self.status.setobsolete(old_docpath)

         # Document integration
         if self.integ.dodocinteg(docnamelist):
            self.integ.obsoleteupdate(old_docnamelist)

         self.commit(old_docnamelist, \
                     self.conf.obsolete+"Status set to obsolete")
         # Remove file from workspace
         self.cmd.rmtree(self.link.const_checkoutpath(old_docnamelist))
      return message

   def editdocument(self, docnamelist):
      """ Edit the document. """
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
      self.cmd.launch_editor(docnamelist)   

   def viewdocument(self, docnamelist):   
      """ View the document. """
      self.export(docnamelist)
      self.cmd.launch_viewer(docnamelist)   
      
   def newissue(self, docnamelist):
      """ Create new issue of the document. """
      new_issue = str(self.getissueno(docnamelist) + 1)
      new_docnamelist = self.setissueno(docnamelist, new_issue)
      docname = self.link.const_docname(new_docnamelist)
      docurl=self.link.const_docurl(new_docnamelist)
      docfileurl=self.link.const_docfileurl(new_docnamelist)
      docpath = self.link.const_docpath(new_docnamelist)
      checkoutpath=self.link.const_checkoutpath(new_docnamelist)
      message = " Created "+docname

      # Create document url in repository
      self.client.mkdir(docurl, "Document directory created", 1)

      # Copy issue to new issue
      self.svncmd.server_side_copy(self.link.const_docfileurl(docnamelist), \
                                   docfileurl, message)
      self.client.checkout(docurl, checkoutpath)

      # Document integration
      if self.integ.dodocinteg(new_docnamelist):
         self.integ.setallfields(new_docnamelist, \
                                 self.gettitle(new_docnamelist), \
                                 self.getkeywords(new_docnamelist), \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document status and commit document
      self.status.setpreliminary(docpath)
      self.client.checkin(docpath, self.conf.newdoc+\
                          "Commited document properties")
      return message   

   def changetitle(self, docnamelist, doctitle):
      """ Change document title. """
      wascheckedout = True
      docpath = self.link.const_docpath(docnamelist)
      
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
         wascheckedout = False

      # Set document title and commit document
      self.settitle(doctitle, docpath)
      self.client.checkin(docpath, self.conf.newtitle+ \
                          "Changed document title")
      if not wascheckedout:
         self.checkin(docnamelist)

   def changekeywords(self, docnamelist, dockeywords):
      """ Change document keywords. """
      wascheckedout = True
      docpath = self.link.const_docpath(docnamelist)
      
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
         wascheckedout = False

      # Set document keywords and commit document
      self.setkeywords(doctitle, dockeywords)
      self.client.checkin(docpath, self.conf.newkeywords+ \
                          "Changed document keywords")
      if not wascheckedout:
         self.checkin(docnamelist)

   def getauthor(self, path):
      """ Get commit author. """
      return self.client.info(path).commit_author

   def getdate(self, path):
      """ Get commit date. """
      return self.client.info(path).commit_time
   
   def getissueno(self, docnamelist):
      """ Get document issue number. """ 
      return int(docnamelist[4])

   def setissueno(self, docnamelist, issue_no):
      """ Set document issue number. """ 
      returnlist = docnamelist[:4]
      returnlist.extend([issue_no, docnamelist[5]])
      return returnlist

   def gettitle(self, docnamelist):
      """ Get document title. """ 
      return self.client.propget(self.conf.proplist[0], \
                           self.link.const_docurl(docnamelist)).values().pop()

   def getkeywords(self, docnamelist):
      """ Get document keywords. """ 
      return self.client.propget(self.conf.proplist[3], \
                  self.link.const_docurl(docnamelist)).values().pop()

   def settitle(self, doctitle, docpath):
      """ Set document title. """ 
      self.client.propset(self.conf.proplist[0], doctitle, docpath)

   def setsvnkeywords(self, docpath):
      """ Set svn keywords. """  
      self.client.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                          docpath) 

   def setkeywords(self, dockeywords, docpath):
      """ Set document keywords. """ 
      self.client.propset(self.conf.proplist[3], dockeywords, docpath)

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
   
   def reverttohead(self, docnamelist):
      """ Revert to head revision undo local changes. """
      return None #fixme
   
   def reverttoprerev(self, docnamelist):
      """ Revert to previous revision. """
      return None #fixme

################################################################################

class docstatus:
   def __init__(self):
      """ Initialize document status class. """
      self.client = pysvn.Client()
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()

   def getstatus(self, docnamelist):
      """ Get document status. """ 
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
      """ Return true if document is preliminary. """
      if self.getstatus(docnamelist) == self.conf.statuslist[0]:
         return True
      else:
         return False

   def isreleased(self, docnamelist):
      """ Return true if document is released. """
      if self.getstatus(docnamelist) == self.conf.statuslist[4]:
         return True
      else:
         return False

   def isnotreleased(self, docnamelist):
      """ Return true if document is not released. """
      return not self.isreleased(docnamelist)

   def isobsolete(self, docnamelist):
      """ Return true if document is obsolete. """
      if self.getstatus(docnamelist) == self.conf.statuslist[5]:
         return True
      else:
         return False

   def isreadonly(self, docnamelist):
      """ Return true if document status implies read-only. """
      if self.isreleased(docnamelist) or self.isobsolete(docnamelist):
         return True
      else:
         return False
