#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  8 22:45:06 2009 on violator
# update count: 259
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

cmd = lowlevel.command()
conf = lowlevel.config()
link = lowlevel.linkname()
db = database.sqlitedb()

def main():
  usage = """usage: %prog REPOS REV
  #
  #Run post-commit options on a repository revision."""

  parser = OptionParser(usage=usage)
 
  (opts,(repos, rvn)) = parser.parse_args()

  # Search patterns for action selection
  newdocptrn = re.compile(conf.newdoc)
  newdoctptrn = re.compile(conf.newdoctype)
  newprojptrn = re.compile(conf.newproj)
  newtitleptrn = re.compile(conf.newtitle)
  newkeywptrn = re.compile(conf.newkeywords)
  obsptrn = re.compile(conf.obsolete)
  relptrn = re.compile(conf.release)
  statchgptrn = re.compile(conf.statchg)
  
  # Construct svnlook command 
  look = lowlevel.svnlook(conf.svnlook, repos, rvn, "--revision")
  
  # Get info about commit
  log_message = look.getlogmsg()
  docfname = look.getdocfname()
  author = look.getauthor()
  date = look.getdate()
  
  if newprojptrn.match(log_message):
    projname = newprojptrn.sub("",log_message)
    category = look.getcategory()
    project = look.getproject()
    writestr = [category, project, projname, author, date]
    db.writeprojlist(rvn, writestr)

  if newdoctptrn.match(log_message):
    db.doctypechg(look.getcategory(), look.getproject(), look.getdoctype())
  
  if docfname:
    # create docname list
    docnamelist = link.deconst_docfname(docfname)
    docurl = link.const_docinrepopath(docnamelist)

    # Get document properties
    doctitle = look.gettitle(docurl)
    status = look.getstatus(docurl)
    dockeywords = look.getkeywords(docurl)

    writestr=[]
    writestr.extend(docnamelist)
    if newdocptrn.match(log_message):
      log_message = newdocptrn.sub("", log_message)
      # Create write string
      writestr.extend([doctitle, status, author, dockeywords, date, "", ""])
      # Write data to db
      db.writedoclist(rvn, writestr)

    if relptrn.match(log_message) or obsptrn.match(log_message):
      log_message = relptrn.sub("", log_message)
      log_message = obsptrn.sub("", log_message)
      db.statuschg(docnamelist, status, date)

    if newtitleptrn.match(log_message):
      log_message = newtitleptrn.sub("", log_message)
      db.titlechg(docnamelist, doctitle)

    if newkeywptrn.match(log_message):
      log_message = newkeywptrn.sub("", log_message)
      db.keywordchg(docnamelist, dockeywords)

    # Write revision list
    writestr = writestr[0:5]
    writestr.append(date)
    writestr.extend([author, log_message])
    # Write data to db
    db.writerevlist(rvn, writestr) 
   
if __name__ == "__main__":
  import sys
  sys.exit(main())
