#!/usr/bin/env python
# $Id$
# Last modified Tue Apr 21 12:57:01 2009 on violator
# update count: 155
# -*- coding:  utf-8 -*-

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


