#!/usr/bin/env python
# $Id$
# Last modified Sun Mar 15 20:03:23 2009 on violator
# update count: 112
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

from optparse import OptionParser

import re
import string

from subdms import lowlevel
from subdms import database

conf = lowlevel.config()
docs = lowlevel.docname()
db = database.sqlitedb()

def command_output(cmd):
  " Capture a command's standard output. "
  import subprocess
  return subprocess.Popen(
      cmd.split(), stdout=subprocess.PIPE).communicate()[0]

def main():
  usage = """usage: %prog REPOS TXN
  #
  #Run pre-commit options on a repository transaction."""

  parser = OptionParser(usage=usage)
 
  (opts,(repos, rvn)) = parser.parse_args()

  # Search patterns for action selection
  newdocptrn = re.compile(conf.newdoc)
  newprojptrn = re.compile(conf.newproj)

  # Construct svnlook command 
  look_opt = "--revision"
  svn_look = "/usr/bin/svnlook"
  look_cmd = "%s %s %s %s %s" % (svn_look, "%s", repos, look_opt, rvn)
  look_cmd2 = "%s %s %s %s %s" % (svn_look, "propget", repos, "%s", "%s")

  # Get info about commit
  log_message = command_output(look_cmd % "log").rstrip("\n").rstrip()
  changed = command_output(look_cmd % "changed")
  docname = changed.split("/").pop().rstrip("\n").rstrip()

  if newprojptrn.match(log_message):
    # Get project name 
    projname = log_message.split(": ")[-1]

    # Write data to db
    db.writeprojlist(projname, conf.doctypes)
     
  if docname:
    # create docname list
    docnamelist = docs.decons_docfname(docname)
    docurl = docs.const_docinrepopath(docnamelist)

    # Get author, date and other properties
    author = command_output(look_cmd % "author").rstrip("\n")
    date = command_output(look_cmd % "date").rstrip("\n")
    title = command_output(look_cmd2 % ("title", docurl))
    status = command_output(look_cmd2 % ("status", docurl))

    if newdocptrn.match(log_message):
      # Create write string
      writestr=[]
      writestr.extend(docnamelist)
      writestr.extend([title, date, status, author, log_message])
      # Write data to db
      db.writerevlist(rvn, writestr)

if __name__ == "__main__":
  import sys
  sys.exit(main())
