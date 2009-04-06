#!/usr/bin/env python
# $Id$
# Last modified Mon Apr  6 21:13:13 2009 on violator
# update count: 159
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
docs = lowlevel.docname()
db = database.sqlitedb()

def main():
  usage = """usage: %prog REPOS TXN
  #
  #Run pre-commit options on a repository transaction."""

  parser = OptionParser(usage=usage)
 
  (opts,(repos, rvn)) = parser.parse_args()

  # Search patterns for action selection
  tmplptrn = re.compile(conf.tmpl)
  newdocptrn = re.compile(conf.newdoc)
  newprojptrn = re.compile(conf.newproj)
  statchgptrn = re.compile(conf.statchg)
  relptrn = re.compile(conf.release)
  obsptrn = re.compile(conf.obsolete)
  
  # Construct svnlook command 
  look = lowlevel.svnlook(repos, rvn)
  
  # Get info about commit
  log_message = look.getlogmsg()
  changed = look.getchanged()
  docfname = look.getdocfname()

  if newprojptrn.match(log_message):
    db.writeprojlist(look.getproject(), conf.doctypes)
     
  if docfname:
    # create docname list
    docnamelist = docs.deconst_docfname(docfname)
    docurl = docs.const_docinrepopath(docnamelist)

    # Get author, date and other properties
    author = look.getauthor()
    date = look.getdate()

    if tmplptrn.match(log_message):
      tmplname, filetype = docfname.split(".")
      db.writetmpllist(rvn, tmplname, filetype, tmplptrn.sub("",log_message))
    else:
      title = look.gettitle(docurl)
      status = look.getstatus(docurl)

    if newdocptrn.match(log_message):
      # Create write string
      writestr=[]
      writestr.extend(docnamelist)
      writestr.extend([title, date, status, author, \
                       newdocptrn.sub("",log_message)])
      # Write data to db
      db.writerevlist(rvn, writestr)

    if relptrn.match(log_message) or obsptrn.match(log_message):
      db.statuschg(docnamelist, status)

        
if __name__ == "__main__":
  import sys
  sys.exit(main())
