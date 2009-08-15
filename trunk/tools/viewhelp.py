#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Mon Aug  3 20:00:01 2009 on violator
# update count: 145
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


from helpviewui import helpView
from subdms import icondict
from subdms import lowlevel

conf = lowlevel.config()
icons = icondict.iconDict()
icons.addIconPath([conf.iconpath])
helpview = helpView(conf.helppath, 'Subdms Documentation', icons)

helpview.show()