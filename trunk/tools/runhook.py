#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  8 22:51:13 2009 on violator
# update count: 157
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

from optparse import OptionParser

from subdms import lowlevel

cmd = lowlevel.command()
conf = lowlevel.config()
link = lowlevel.linkname()

def main():
  usage = """usage: %prog REV """

  parser = OptionParser(usage=usage)
 
  (opts,(rvn, )) = parser.parse_args()

  repohook = "post-commit"
  
  revhookpath = link.const_repohookpath(repohook)
  repopath = conf.repopath

  cmd.command_output(revhookpath+" "+repopath+" "+rvn)
if __name__ == "__main__":
  import sys
  sys.exit(main())


