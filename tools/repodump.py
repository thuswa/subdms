#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  8 22:51:05 2009 on violator
# update count: 139
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

from subdms import lowlevel

svncmd = lowlevel.svncmd()
conf = lowlevel.config()

# Dump database
for item in svncmd.recursivels(conf.repourl):
    print(item["name"])


