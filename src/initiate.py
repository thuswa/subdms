#!/usr/bin/env python
# $Id$
# Last modified Wed Mar 11 00:25:11 2009 on violator
# update count: 91
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil

import config
import database
import frontend

conf = config.dmsconfig()
client = pysvn.Client()

# set some vars
projname="project"
nrdocs=2;

# create workspace directory
if not os.path.isdir(conf.workpath):
    os.makedirs(conf.workpath)

# create db
db = database.sqlitedb(conf.dbpath)
db.createdb()

# create subversion repository and layout
frontend.createrepo()

# install templates
frontend.installtemplates()

# install hooks
frontend.installhooks()

# copy hook to repo dir
#cp post-commit ./$REPONAME/hooks
#chmod +x ./$REPONAME/hooks/post-commit

# create project layout and add some docs
frontend.createproject("test")

docnamelist1=['test','note','0001','txt']
doctitle1='Test note'
frontend.createdocument(docnamelist1, doctitle1)
docnamelist2=['test','list','0001','txt']
doctitle2='Test list'
frontend.createdocument(docnamelist2, doctitle2)
docnamelist3=['test','list','0002','txt']
doctitle3='Test list2'
frontend.createdocument(docnamelist3, doctitle3)

# Dump database
db.dumpdb()

print db.getdocno("test", "list")


 

