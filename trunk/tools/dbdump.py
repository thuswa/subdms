#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 29 14:27:43 2009 on violator
# update count: 132
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

from subdms import database

db = database.sqlitedb()

# Dump database
print "Document list:"
for row in db.getalldocs():
    print row
print "Template list:"
for row in db.getalltmpls():
    print row
print "Project list:"
for row in db.dumpallprojs(): 
    print row
print "Revision list:"
for row in db.getallrev():
    print row 

