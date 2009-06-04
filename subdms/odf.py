#!/usr/bin/env python
# $Id$
# Last modified Fri Jun  5 00:45:31 2009 on violator
# update count: 543
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
import zipfiles

import lowlevel

"""
Open Document Fromat user fields manipulation class. 
"""

class odfuserfields:
    def __init__(self):
        """ Initialize odfuserfield class """
        self.conf = lowlevel.config()

    def openfile(self, docpath):
        """ Read odf file and extract contents.xml file. """
        self.file = zipfile.ZipFile(docpath, "r")


    def updatefields(self):
        """ Update user fields and write back contents.xml file. """

    def closefile()
        """ Close odf file. """   
        self.file.close()
