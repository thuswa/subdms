#!/usr/bin/env python
# $Id$
# Last modified Thu Mar 12 14:14:33 2009 on havoc
# update count: 108
# -*- coding:  utf-8 -*-

import database
import frontend
import lowlib

conf = lowlib.dmsconfig()
db = database.sqlitedb()

# create project layout and add some docs
frontend.createproject("test")

docnamelist1=frontend.createdocnamelist('test','note','txt')
doctitle1='Test note'
frontend.createdocument(docnamelist1, doctitle1)
docnamelist2=frontend.createdocnamelist('test','note','txt')
doctitle2='Test list'
frontend.createdocument(docnamelist2, doctitle2)
docnamelist3=frontend.createdocnamelist('test','list','txt')
doctitle3='Test list2'
frontend.createdocument(docnamelist3, doctitle3)

# Dump database
print db.getalldocs()
print db.getallprojs()

print db.getdocno("test", "list")
