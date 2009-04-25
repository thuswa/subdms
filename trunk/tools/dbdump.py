#!/usr/bin/env python
# $Id$
# Last modified Sat Apr 25 23:53:13 2009 on violator
# update count: 130
# -*- coding:  utf-8 -*-

from subdms import database

db = database.sqlitedb()

# Dump database
print "Document list:"
for row in db.getalldocs():
    print row
print "Template list:"
for row in db.getalltmpls():
    print row
print "Project list:"
for row in db.dumpallprojs(): 
    print row
print "Revision list:"
for row in db.getallrev():
    print row 

