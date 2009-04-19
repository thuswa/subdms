#!/usr/bin/env python
# $Id$
# Last modified Mon Apr 20 00:16:57 2009 on violator
# update count: 117
# -*- coding:  utf-8 -*-

from subdms import database

db = database.sqlitedb()

# Dump database
print db.getalldocs()
print db.getalltmpls()
print db.getallprojs()
print db.getallrev()

