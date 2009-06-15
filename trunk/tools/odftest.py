#!/usr/bin/env python
# $Id$
# Last modified Mon Jun 15 22:21:26 2009 on violator
# update count: 151
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

ouf = odf.odfuserfields()
cmd = lowlevel.command()
link = lowlevel.linkname()

docnamelist = ['P','DDF','SPEC','0002','1','odt'] 

docpath = link.const_docpath(docnamelist)
doczippath = link.const_doczippath(docnamelist)

# Rename odf file
cmd.renamefile(docpath, doczippath)

# Update fields and write contents back to odf file
contentstr = ouf.extractcontent(doczippath)
contentstr = ouf.updatefields(contentstr, fieldcodes, \
                                   fieldcontents)
ouf.writecontent(docpath, contentstr)

# Close files and delete zip file
ouf.closefiles()
cmd.rm(doczippath)
