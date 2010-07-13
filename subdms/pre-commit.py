#!/usr/bin/python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  8 22:45:20 2009 on violator
# update count: 261
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
import re

from subdms import lowlevel

""" pre-commit hook to restrict commits. """

conf = lowlevel.config()
link = lowlevel.linkname()

def main():
  usage = """usage: %prog REPOS TXN
  #
  #Run pre-commit options on a repository transaction."""

  parser = OptionParser(usage=usage)

  # Search patterns for action selection
  newdocptrn = re.compile(conf.newdoc)
  obsptrn = re.compile(conf.obsolete)
  relptrn = re.compile(conf.release)
 
  errors = 0
  status = conf.statuslist[0]
  (opts, (repos, txn)) = parser.parse_args()

  # Construct svnlook command
  look = lowlevel.svnlook(conf.svnlook, repos, txn, "--transaction")      
  # Get info about commit
  docfname = look.getdocfname()

  if docfname:
    # create docname list
    docnamelist = link.deconst_docfname(docfname)
    docurl = link.const_docinrepopath(docnamelist)

    log_message = look.getlogmsg()
    status = look.getstatus(docurl)

    if not relptrn.match(log_message) and not obsptrn.match(log_message) \
           and not newdocptrn.match(log_message):
      if status in conf.statuslist[4:6]:
        errors = 1
        print(docfname+" is "+status+" and thus read-only.") 
  return errors
  
if __name__ == "__main__":
  import sys
  sys.exit(main())

