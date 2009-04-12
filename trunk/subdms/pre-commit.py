#!/usr/bin/python
# $Id$
# Last modified Thu Apr  9 23:23:21 2009 on violator
# update count: 83

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
  look = lowlevel.svnlook(repos, txn, "--transaction")      
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
        print docfname+" is "+status+" and thus read-only." 
  return errors
  
if __name__ == "__main__":
  import sys
  sys.exit(main())

