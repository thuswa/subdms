#!/usr/bin/env python
# $Id$
# Last modified Mon Jun 29 00:39:24 2009 on violator
# update count: 197
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

from subdms import odf
from subdms import lowlevel
from subdms import integration

ouf = odf.odfuserfields()
integ = integration.docinteg()
cmd = lowlevel.command()
link = lowlevel.linkname()

docnamelist = ['P','DDF','SPEC','0002','1','odt'] 

doctitle = "Test document title"
status = "preliminary"
author = "jondoe"
dockeywords = "Test, document, odf, integration"

fields = integ.const_fields(docnamelist, doctitle, dockeywords, author, status)

docpath = link.const_docpath(docnamelist)
doczippath = link.const_doczippath(docnamelist)

print docpath
print doczippath

# Rename odf file
cmd.renamefile(docpath, doczippath)

# Update fields and write contents back to odf file
contentstr = ouf.extractcontent(doczippath)
contentstr = ouf.setuserfields(contentstr, fields)

#print ouf.getfields(contentstr)

ouf.writecontent(docpath, contentstr)

# Close files and delete zip file
ouf.closefiles()
cmd.rm(doczippath)
