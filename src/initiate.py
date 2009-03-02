#!/usr/bin/env python
# $Id$
# Last modified Mon Mar  2 22:47:50 2009 on violator
# update count: 68
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
database.createdb(conf.dbpath)

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

#for n in 1 nrdocs:
docnamelist1=['test','note','0001','txt']
doctitle1='Test note'
frontend.createdocument(docnamelist1, doctitle1)
docnamelist2=['test','list','0001','txt']
doctitle2='Test list'
frontend.createdocument(docnamelist2, doctitle2)


#    svn mkdir --parents  -m "create doc dirs" $URR/$PROJ/$DOC/000$N
#    svn co $URR/$PROJ/$DOC/000$N ./workspace
#    DOCNAME=$PROJNAME-$DOC-000$N".txt"
#    echo "yea it is" > ./workspace/$DOCNAME
#    #	echo $DOCNAME
#    svn add ./workspace/$DOCNAME
#    svn ci -m "initial commit" ./workspace/$DOCNAME
#    rm -rf ./workspace/* ./workspace/.svn




 

