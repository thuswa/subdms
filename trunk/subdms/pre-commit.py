#!/usr/bin/python
# $Id$
# Last modified Tue Apr  7 12:55:38 2009 on violator
# update count: 77

from optparse import OptionParser
import re

from subdms import lowlevel

""" pre-commit hook to restrict commits. """

conf = lowlevel.config()
docs = lowlevel.docname()

def main():
  usage = """usage: %prog REPOS TXN
  #
  #Run pre-commit options on a repository transaction."""

  parser = OptionParser(usage=usage)

  # Search patterns for action selection
  newdocptrn = re.compile(conf.newdoc)
  obsptrn = re.compile(conf.obsolete)
  relptrn = re.compile(conf.release)
  tmplptrn = re.compile(conf.tmpl)
 
  errors = 0
  status = conf.statuslist[0]
  (opts, (repos, txn)) = parser.parse_args()

  # Construct svnlook command
  look = lowlevel.svnlook(repos, txn, "--transaction")      
  # Get info about commit
  docfname = look.getdocfname()

  if docfname:
    # create docname list
    docnamelist = docs.deconst_docfname(docfname)
    docurl = docs.const_docinrepopath(docnamelist)

    log_message = look.getlogmsg()

    if not tmplptrn.match(log_message):
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

