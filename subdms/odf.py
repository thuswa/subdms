#!/usr/bin/env python
# $Id$
# Last modified Sat Jun  6 01:10:12 2009 on violator
# update count: 582
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
        self.file = zipfile.ZipFile(docpath, "r")
        contentstr = self.file.read(self.conf.odfcontent)
        self.closefile()
        return contentstr

    def writecontent(self, docpath, contentstr):
        """ Write content.xml to odf file. """
        self.file = zipfile.ZipFile(docpath, "w", zipfile.ZIP_DEFLATED)
        self.file.writestr(self.conf.odfcontent, contentstr)
        self.closefile()
        
    def updatefields(self, docpath):
        """ Update user fields and write back contents.xml file. """
        #contentstr = self.extractcontent(docpath)
        #doc = xml.dom.minidom.parseString(contentstr)
        #

        # write back file contents of content.xml
        self.writecontent(docpath)
        #print doc
        
    def closefile(self):
        """ Close odf file. """   
        self.file.close()
