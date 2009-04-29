#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 29 14:26:45 2009 on violator
# update count: 109
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

import database
import frontend
import lowlib

conf = lowlib.dmsconfig()
db = database.sqlitedb()

# create project layout and add some docs
frontend.createproject("test")

docnamelist1=frontend.createdocnamelist('test','note','txt')
doctitle1='Test note'
frontend.createdocument(docnamelist1, doctitle1)
docnamelist2=frontend.createdocnamelist('test','note','txt')
doctitle2='Test list'
frontend.createdocument(docnamelist2, doctitle2)
docnamelist3=frontend.createdocnamelist('test','list','txt')
doctitle3='Test list2'
frontend.createdocument(docnamelist3, doctitle3)

# Dump database
print db.getalldocs()
print db.getallprojs()

print db.getdocno("test", "list")
