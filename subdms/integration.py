#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 22 11:32:19 2009 on havoc
# update count: 392
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

import lowlevel
import database

"""
Document integration class. 
"""

class docinteg:
    def __init__(self):
        """ Initialize docinteg """
        self.conf = lowlevel.config()
        self.db = database.sqlitedb()
        self.link = lowlevel.linkname()

    def updateallfields(self, docnamelist):
        """ Update all document fields. """
        docinfo = self.db.getdocumentinfo(docnamelist)
        
        # Name the document info
        proj = docinfo[2]
        issue = docinfo[5]
        [doctitle, status, author, keyw] = docinfo[7:-3]
        rdate = docinfo[12]
        docid = self.link.const_docid(docnamelist)
        
        # Get the document description
        desc = self.db.getprojdesc(proj)

        # Create fieldcontents list
        fieldcontents =[doctitle, docid, issue, status, rdate, author, \
                        proj, desc, keyw]
        
        # Choose action depending on filetype
        if docnamelist[-1] == "tex": 
            self.texfieldupdate(docnamelist, self.conf.fieldcodes, \
                                    fieldcontents)

        
    def texfieldpattern(self, fieldcode, fieldcontent=".*"):
        """ return field code string for tex file. """
        return re.compile(".newcommand .."+fieldcode+". ."+fieldcontent+".")

    def texfieldcode(self, fieldcode, fieldcontent):
        return "\\newcommand {\\"+fieldcode+"} {"+fieldcontent+"}"

    def texfieldupdate(self, docnamelist, fieldcodes, fieldcontents):
        """ Update field codes in document. """
        docpath = self.link.const_docpath(docnamelist)
        print docpath
        for line in fileinput.FileInput(docpath, inplace=1):
            for code, content in map(None, fieldcodes, fieldcontents):
                fieldptrn = self.texfieldpattern(code)
                if fieldptrn.match(line):
                    line = self.texfieldcode(code, content)
            print line.replace("\n","")

       
