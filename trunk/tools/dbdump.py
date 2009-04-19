#!/usr/bin/env python
# $Id$
# Last modified Mon Apr 20 00:22:31 2009 on violator
# update count: 122
# -*- coding:  utf-8 -*-

from subdms import database

db = database.sqlitedb()

# Dump database
print "Document list:"
print db.getalldocs()
print "Template list:"
print db.getalltmpls()
print "Project list:"
print db.getallprojs()
print "Revision list:"
print db.getallrev()

