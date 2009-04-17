#!/usr/bin/env python
# $Id$
# Last modified Fri Apr 17 21:28:37 2009 on violator
# update count: 203
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

cmd = lowlevel.command()
conf = lowlevel.config()
link = lowlevel.linkname()
db = database.sqlitedb()

def main():
  usage = """usage: %prog REPOS REV
  #
  #Run pre-commit options on a repository transaction."""

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
  look = lowlevel.svnlook(repos, rvn, "--revision")
  
  # Get info about commit
  log_message = look.getlogmsg()
  docfname = look.getdocfname()

  if newprojptrn.match(log_message):
    description = newprojptrn.sub("",log_message)
    db.writeprojlist(look.getcategory(), look.getproject(), description)

  if newdoctptrn.match(log_message):
    db.doctypechg(look.getcategory(), look.getproject(), look.getdoctype())
  
  if docfname:
    # create docname list
    docnamelist = link.deconst_docfname(docfname)
    docurl = link.const_docinrepopath(docnamelist)

    # Get author, date and other properties
    author = look.getauthor()
    date = look.getdate()
    doctitle = look.gettitle(docurl)
    status = look.getstatus(docurl)
    dockeywords = look.getkeywords(docurl)
    
    if newdocptrn.match(log_message):
      # Create write string
      writestr=[]
      writestr.extend(docnamelist)
      writestr.extend([doctitle, date, status, author, dockeywords, \
                       newdocptrn.sub("",log_message)])
      # Write data to db
      db.writerevlist(rvn, writestr)

    if relptrn.match(log_message) or obsptrn.match(log_message):
      db.statuschg(docnamelist, status)

    if newtitleptrn.match(log_message):
      db.titlechg(docnamelist, doctitle)

    if newkeywptrn.match(log_message):
      db.keywordchg(docnamelist, dockeywords)
      
if __name__ == "__main__":
  import sys
  sys.exit(main())
