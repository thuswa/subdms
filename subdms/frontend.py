#!/usr/bin/env python
# $Id$
# Last modified Fri May  1 22:10:11 2009 on violator
# update count: 1127
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

import integration
import lowlevel

""" Front-end classes. """

class project:
   def __init__(self):
      """ Initialize project class """
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()
      self.svncmd = lowlevel.svncmd()
      
   def createcategory(self, category):
      """ Create category dir in repo. """
      self.svncmd.mkdir(self.link.const_caturl(category), "Created a category")
      
   def createproject(self, category, project, projname, doctypes):
      """ Create project dir in repo. """
      self.svncmd.mkdir(self.link.const_projurl(category, project), \
                        self.conf.newproj+projname)
      self.adddoctypes(category, project, doctypes)

   def adddoctypes(self, category, project, doctypes):
      """ Add new doctypes. """
      for doc in doctypes:
         self.svncmd.mkdir(self.link.const_doctypeurl(category, project, doc), \
                           self.conf.newdoctype+"Added doctype")
      
################################################################################

class document:
   def __init__(self):
      """ Initialize project class """
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
      self.svncmd.mkdir(docurl, "Document directory created.")
      
      # Create document from template or existing document
      self.svncmd.server_side_copy(createfromurl, docfileurl, \
                                   "Document created")
      self.svncmd.checkout(docurl, checkoutpath)

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.setallfields(docnamelist, doctitle, dockeywords, \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document title and commit document
      self.settitle(docpath, doctitle)
      self.setkeywords(docpath, dockeywords)
      self.status.setpreliminary(docpath)

      self.svncmd.checkin(docpath, self.conf.newdoc+ \
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
      self.svncmd.mkdir(docurl, "Document directory created.")
      self.svncmd.checkout(docurl, checkoutpath)
      
      # Copy file to workspace
      self.cmd.copyfile(addfilepath, docpath)
      self.svncmd.add(docpath)

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.setallfields(docnamelist, doctitle, dockeywords, \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document title and commit document
      self.settitle(docpath, doctitle)
      self.setkeywords(docpath, dockeywords)
      self.setsvnkeywords(docpath)
      self.status.setpreliminary(docpath)

      self.svncmd.checkin(docpath, self.conf.newdoc+ \
                          "Commited document properties.")

   def commit(self, docnamelist, message):
      """ Commit changes on file. """
      self.svncmd.checkin(self.link.const_docpath(docnamelist), message)

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
      self.svncmd.checkout(self.link.const_docurl(docnamelist), \
                           self.link.const_checkoutpath(docnamelist))
      #  self.client.lock( 'file.txt', 'reason for locking' )

   def export(self, docnamelist):
      """ Export file to workspace. """
      checkoutpath = self.link.const_readonlypath(docnamelist)
      docpath = self.link.const_readonlyfilepath(docnamelist)
#      self.cmd.rmtree(checkoutpath)
      self.svncmd.export(self.link.const_docurl(docnamelist), checkoutpath)
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
         self.obsolete(old_docnamelist)           
      return message

   def obsolete(self, docnamelist):
      """ Obsolete the document. """
      docpath = self.link.const_docpath(docnamelist)
      docurl = self.link.const_docurl(docnamelist)
      self.svncmd.checkout(docurl, self.link.const_checkoutpath(docnamelist))
      self.status.setobsolete(docpath)
      message = "Status set to obsolete"
      
      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.obsoleteupdate(docnamelist)
         self.commit(docnamelist, self.conf.obsolete+"Status set to obsolete")
         # Remove file from workspace
         self.cmd.rmtree(self.link.const_checkoutpath(docnamelist))
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
      message = "New issue created."

      # Create document url in repository
      self.svncmd.mkdir(docurl, "Document directory created")

      # Copy issue to new issue
      self.svncmd.server_side_copy(self.link.const_docfileurl(docnamelist), \
                                   docfileurl, message)
      self.svncmd.checkout(docurl, checkoutpath)

      # Document integration
      if self.integ.dodocinteg(new_docnamelist):
         self.integ.setallfields(new_docnamelist, \
                                 self.gettitle(new_docnamelist), \
                                 self.getkeywords(new_docnamelist), \
                                 self.getauthor(checkoutpath), \
                                 self.conf.statuslist[0])

      # Set document status and commit document
      self.status.setpreliminary(docpath)
      self.svncmd.checkin(docpath, self.conf.newdoc+\
                          "Commited document properties")
      return message   

   def changetitle(self, docnamelist, doctitle):
      """ Change document title. """
      wascheckedout = True
      docpath = self.link.const_docpath(docnamelist)
      
      if not self.ischeckedout(docnamelist):
         self.checkout(docnamelist)
         wascheckedout = False

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.updatetitle(docnamelist, doctitle)

      # Set document title and commit document
      self.settitle(docpath, doctitle)
      self.svncmd.checkin(docpath, self.conf.newtitle+ \
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

      # Document integration
      if self.integ.dodocinteg(docnamelist):
         self.integ.updatekeywords(docnamelist, dockeywords)

      # Set document keywords and commit document
      self.setkeywords(docpath, dockeywords)
      self.svncmd.checkin(docpath, self.conf.newkeywords+ \
                          "Changed document keywords")
      if not wascheckedout:
         self.checkin(docnamelist)

   def getauthor(self, path):
      """ Get commit author. """
      return self.svncmd.info(path).commit_author

   def getdate(self, path):
      """ Get commit date. """
      return self.svncmd.info(path).commit_time
   
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
      return self.svncmd.propget(self.conf.proplist[0], \
                                 self.link.const_docurl(docnamelist))

   def getkeywords(self, docnamelist):
      """ Get document keywords. """ 
      return self.svncmd.propget(self.conf.proplist[3], \
                                 self.link.const_docurl(docnamelist))

   def settitle(self, docpath, doctitle):
      """ Set document title. """ 
      self.svncmd.propset(self.conf.proplist[0], doctitle, docpath)

   def setsvnkeywords(self, docpath):
      """ Set svn keywords. """  
      self.svncmd.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                          docpath) 

   def setkeywords(self, docpath, dockeywords):
      """ Set document keywords. """ 
      self.svncmd.propset(self.conf.proplist[3], dockeywords, docpath)

   def ischeckedout(self, docnamelist):
      """ Return true if docname is checked out. """
      return self.cmd.workingcopyexists(docnamelist)

   def getstate(self, docnamelist):
      """ Get document state. """
      if self.ischeckedout(docnamelist):
         docpath = self.link.const_docpath(docnamelist)
         state = self.svncmd.status(docpath)
         return_state = ['O', 'Checked Out']
         if state.text_status == self.svncmd.modified:
            return_state = ['M', 'Modified']
         if state.text_status == self.svncmd.conflicted:
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
      self.conf = lowlevel.config()
      self.link = lowlevel.linkname()
      self.svncmd = lowlevel.svncmd()
      
   def getstatus(self, docnamelist):
      """ Get document status. """ 
      return self.svncmd.propget(self.conf.proplist[1],
                                 self.link.const_docurl(docnamelist))

   def setpreliminary(self, docpath):
      """ Set document status to preliminary. """ 
      self.svncmd.propset(self.conf.proplist[1], \
                          self.conf.statuslist[0], docpath)

   def setreleased(self, docpath):
      """ Set document status to released. """ 
      self.svncmd.propset(self.conf.proplist[1], self.conf.statuslist[4], \
                          docpath)

   def setobsolete(self, docpath):
      """ Set document status to obsolete. """
      self.svncmd.propset(self.conf.proplist[1], self.conf.statuslist[5], \
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
