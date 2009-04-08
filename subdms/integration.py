#!/usr/bin/env python
# $Id$
# Last modified Wed Apr  8 21:21:13 2009 on violator
# update count: 252
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

import lowlevel

"""
Document integration class. 
"""

class docinteg:
    def __init__(self):
        """ Initialize docinteg """
        self.conf = lowlevel.config()

        
    def createdb(self):
