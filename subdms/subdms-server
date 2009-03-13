#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 00:32:20 2009 on violator
# update count: 134
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil
import string
import subprocess 

from subdms import lowlevel, database, repository

conf = lowlevel.dmsconfig()
repo = repository.repository()

# create workspace directory
if not os.path.isdir(conf.workpath):
    os.makedirs(conf.workpath)

# create db
db = database.sqlitedb()
db.createdb()

# create subversion repository and layout
repo.createrepo()

# install templates
repo.installtemplates()

# install hooks
repo.installhooks()

