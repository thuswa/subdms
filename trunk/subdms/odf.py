#!/usr/bin/env python
# $Id$
# Last modified Mon Jun 29 00:41:51 2009 on violator
# update count: 718
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

import string
import re
import xml.dom.minidom
import zipfile

import lowlevel

"""
Open Document Format user fields manipulation class. 
"""

class odfuserfields:
    def __init__(self):
        """ Initialize odfuserfield class """
        self.conf = lowlevel.config()

    def extractcontent(self, docpath):
        """ Read odf file and extract contents.xml file. """
        self.infile = zipfile.ZipFile(docpath, "r")
        return self.infile.read(self.conf.odfcontent)

    def writecontent(self, docpath, contentstr):
        """ Write content back to odf file. """
        self.outfile = zipfile.ZipFile(docpath, "w", zipfile.ZIP_DEFLATED)
        for item in self.infile.infolist():
            buffer = self.infile.read(item.filename)
            if item.filename  == self.conf.odfcontent:
                self.outfile.writestr(item, contentstr)
            else:
                self.outfile.writestr(item, buffer)
        
    def getuserfields(self, contentstr):
        """ Just read the user fields from an XML file."""
        doc = xml.dom.minidom.parseString(contentstr)
        ufds = doc.getElementsByTagName('text:user-field-decls')
        fieldlist = []
        for fields in ufds:
            for field in fields.childNodes:
                fieldlist.append(field.attributes.items())
        return fieldlist            

    def setuserfields(self, contentstr, fields):
        """ Set the user fields in content file."""
        # Parse xml string to dom doc
        doc = xml.dom.minidom.parseString(contentstr)

        # Get user field declarations and loop through them
        ufds = doc.getElementsByTagName('text:user-field-decls')
        for userfields in ufds:
            for userfield in userfields.childNodes:
                userkey = userfield.attributes.getNamedItem('text:name').value
                userfield.setAttribute('office:value',fields[userkey])
                userfield.setAttribute('office:value-type', 'string')

        # Write back dom tree to string and unlink        
        contentstr = doc.toxml()
        doc.unlink()
        return contentstr            

    def closefiles(self):
        """ Close odf files. """   
        self.infile.close()
        self.outfile.close()
        
