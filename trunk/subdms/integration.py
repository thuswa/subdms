#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 29 13:01:43 2009 on violator
# update count: 487
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

import fileinput
import string
import re

import database
import epoch
import lowlevel

"""
Document integration class. 
"""

class docinteg:
    def __init__(self):
        """ Initialize docinteg """
        self.conf = lowlevel.config()
        self.db = database.sqlitedb()
        self.dt = epoch.dtime()
        self.link = lowlevel.linkname()

    def setallfields(self, docnamelist, doctitle, dockeywords, author, status):
        """ Update all document fields. """
        # Name the document info
        cat = docnamelist[0]
        proj = docnamelist[1]
        issue = docnamelist[-2]
        rdate = ""
        docid = self.link.const_docid(docnamelist)

        # Get the project name
        projname = self.db.getprojname(cat, proj)
        
        # Create fieldcontents list
        fieldcontents =[doctitle, docid, issue, status, rdate, author, \
                        projname, dockeywords]
        
        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, self.conf.fieldcodes, \
                                    fieldcontents)

    def updatetitle(self, docnamelist, doctitle):
        """ Update the title field. """
        fieldcontents = [doctitle]
        fieldcodes = self.conf.fieldcodes[0:1]

        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, fieldcodes, fieldcontents)
        
    def updatekeywords(self, docnamelist, dockeywords):
        """ Update the keywords field. """
        fieldcontents = [dockeywords]
        fieldcodes = self.conf.fieldcodes[7]
        
        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, fieldcodes, fieldcontents)
        
    def releaseupdate(self, docnamelist):
        """ Update the release date and status field. """
        fieldcontents = [self.conf.statuslist[4], self.dt.datestamp()]
        fieldcodes = self.conf.fieldcodes[3:5]
        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, fieldcodes, fieldcontents)

    def obsoleteupdate(self, docnamelist):
        """ Update the release date and status field. """
        fieldcontents = [self.conf.statuslist[5]+" "+self.dt.datestamp()] 
        fieldcodes = self.conf.fieldcodes[3]
        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, fieldcodes, fieldcontents)
    
    def texfieldpattern(self, fieldcode, fieldcontent=".*"):
        """ return field code string for tex file. """
        return re.compile(".newcommand .."+fieldcode+". ."+fieldcontent+".")

    def texfieldcode(self, fieldcode, fieldcontent):
        return "\\newcommand {\\"+fieldcode+"} {"+fieldcontent+"}"

    def texfieldupdate(self, docnamelist, fieldcodes, fieldcontents):
        """ Update field codes in document. """
        docpath = self.link.const_docpath(docnamelist)
        for line in fileinput.FileInput(docpath, inplace=1):
            for code, content in map(None, fieldcodes, fieldcontents):
                fieldptrn = self.texfieldpattern(code)
                if fieldptrn.match(line):
                    line = self.texfieldcode(code, content.replace("\n", r"\\"))
            print line.replace("\n","")

    def dodocinteg(self, docnamelist):
        """ Check if document integration should be done. """
        if docnamelist[-1] in self.conf.integtypes \
               and docnamelist[0] != self.conf.categories[1]:
            return True
        else:
            return False
