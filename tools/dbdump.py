#!/usr/bin/env python
# $Id$
# Last modified Mon Apr 20 00:32:43 2009 on violator
# update count: 129
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
for row in db.getallprojs(): 
    print row
print "Revision list:"
for row in db.getallrev():
    print row 

