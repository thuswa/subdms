#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  7 20:48:37 2010 on stalker
# update count: 723
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

import codecs
import string
import re

# from . import database # Python 3.X
# from . import epoch    # Python 3.X
# from . import lowlevel # Python 3.X
# from . import odf      # Python 3.X
import database
import epoch
import lowlevel
import odf

"""
Document integration class. 
"""

class docinteg:
    def __init__(self):
        """ Initialize docinteg """
        self.cmd = lowlevel.command()
        self.conf = lowlevel.config()
        self.db = database.sqlitedb()
        self.dt = epoch.dtime()
        self.link = lowlevel.linkname()
        self.ouf = odf.odfuserfields()
        self.keys = self.conf.fields 
        
    def setallfields(self, docnamelist, doctitle, dockeywords, author, status):
        """ Update all document fields. """
        fields = self.const_fields(docnamelist, doctitle, dockeywords, author, \
                                   status)
        # Choose action depending on filetype
        self.filetypechooser(docnamelist, fields)
            
    def updatetitle(self, docnamelist, doctitle):
        """ Update the title field. """
        fields = {self.keys[7] : doctitle}

        # Choose action depending on filetype
        self.filetypechooser(docnamelist, fields)
        
    def updatekeywords(self, docnamelist, dockeywords):
        """ Update the keywords field. """
        fields = {self.keys[3] : dockeywords}
        
        # Choose action depending on filetype
        self.filetypechooser(docnamelist, fields)
            
    def releaseupdate(self, docnamelist):
        """ Update the release date and status field. """
        fields = {self.keys[6] : self.conf.statuslist[4], \
                  self.keys[5] : self.dt.datestamp()}

        # Choose action depending on filetype
        self.filetypechooser(docnamelist, fields)

    def obsoleteupdate(self, docnamelist):
        """ Update the release date and status field. """
        fields = {self.keys[6] : self.conf.statuslist[5]+" "+ \
                  self.dt.datestamp()}

        # Choose action depending on filetype
        self.filetypechooser(docnamelist, fields)
    
    def texfieldpattern(self, fieldkey, fieldcontent=".*"):
        """ return field code string for tex file. """
        return re.compile(".newcommand .."+fieldkey+". ."+fieldcontent+".")

    def texfieldcode(self, fieldkey, fieldcontent):
        return "newcommand {\\"+fieldkey+"} {"+fieldcontent+"}"

    def texfieldupdate(self, docnamelist, fields):           
        """ Update field codes in tex document. """
        docpath = self.link.const_docpath(docnamelist)
        doctmppath = self.link.const_doctmppath(docnamelist)

        # Rename tex file
        self.cmd.renamefile(docpath, doctmppath)

        # Update fields and write contents back to tex file
        outfile = codecs.open(docpath, encoding='utf-8', mode='w')
        contentstr = open(doctmppath).read()
        for key,value in fields.items():
            fieldptrn = self.texfieldpattern(key)
            newfield = self.texfieldcode(key, value.replace("\n", r"\\"))
            contentstr = re.sub(fieldptrn, newfield, contentstr)

        outfile.write(contentstr)

        # Close files and delete tmp file
        outfile.close()
        self.cmd.rm(doctmppath)


    def odffieldupdate(self, docnamelist, fields):           
        """ Update field codes in odf document. """
        docpath = self.link.const_docpath(docnamelist)
        doctmppath = self.link.const_doctmppath(docnamelist)

        # Rename odf file
        self.cmd.renamefile(docpath, doctmppath)

        # Update fields and write contents back to odf file
        contentstr = self.ouf.extractcontent(doctmppath)
        contentstr = self.ouf.setuserfields(contentstr, fields)
        self.ouf.writecontent(docpath, contentstr)

        # Close files and delete tmp file
        self.ouf.closefiles()
        self.cmd.rm(doctmppath)
        
    def dodocinteg(self, docnamelist):
        """ Check if document integration should be done. """
        if docnamelist[-1] in self.conf.integtypes \
               and docnamelist[0] != self.conf.categories[1]:
            return True
        else:
            return False
        
    def filetypechooser(self, docnamelist, fields):
        """ Call function depending on file type. """
        if self.conf.isodf(docnamelist):
            self.odffieldupdate(docnamelist, fields)
        elif self.conf.istex(docnamelist):
            self.texfieldupdate(docnamelist, fields)

    def const_fields(self, docnamelist, doctitle, dockeywords, author, status):
        """ Constuct the fields dictionary. """
 
        rdict = {}
        # Name the document info
        cat = docnamelist[0]
        proj = docnamelist[1]

        # Populate the fields dictionary
        rdict[self.keys[0]] = author
        rdict[self.keys[1]] = self.link.const_docid(docnamelist)
        rdict[self.keys[2]] = docnamelist[-2]
        rdict[self.keys[3]] = dockeywords
        rdict[self.keys[4]] = self.db.getprojname(cat, proj)
        rdict[self.keys[5]] = ""
        rdict[self.keys[6]] = status
        rdict[self.keys[7]] = doctitle

        return rdict
