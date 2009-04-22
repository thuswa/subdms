#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 22 23:58:32 2009 on violator
# update count: 89
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

import time

class dtime:
    def datestamp(self):
        """ Returns formatted date string. """
        return time.strftime("%Y-%m-%d")

    def timestamp(self):
        """ Returns formatted time string. """
        return time.strftime("%H:%M:%S")
    
    def datetimestamp(self):
        """ Returns formatted date time string. """
        return self.datestamp()+' '+self.timestamp()
   
    def attime(self):
       """ Prints at timestamp to standard output. """
       print 'At '+self.datetimestamp()  

    def unix2date(self, unixtime):
        """ Converts unix time to date string. """
        return time.strftime("%Y-%m-%d", time.gmtime(unixtime))

    def unix2time(self, unixtime):
        """ Converts unix time to date string. """
        return time.strftime("%H:%M:%S", time.gmtime(unixtime))
