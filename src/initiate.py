#!/usr/bin/env python
# $Id$
# Last modified Thu Feb 26 13:23:54 2009 on havoc
# update count: 45
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil
import subprocess 

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

# create template directory and install templates
if not os.path.isdir(conf.tmplpath):
    os.makedirs(conf.tmplpath)


# create db
database.createdb(conf.dbpath)

# create subversion repository
subprocess.call(['svnadmin','create',conf.repopath])

# copy hook to repo dir
#cp post-commit ./$REPONAME/hooks
#chmod +x ./$REPONAME/hooks/post-commit

# create project layout and add some docs
frontend.createproject("test")


#for n in 1 nrdocs: 
#    svn mkdir --parents  -m "create doc dirs" $URR/$PROJ/$DOC/000$N
#    svn co $URR/$PROJ/$DOC/000$N ./workspace
#    DOCNAME=$PROJNAME-$DOC-000$N".txt"
#    echo "yea it is" > ./workspace/$DOCNAME
#    #	echo $DOCNAME
#    svn add ./workspace/$DOCNAME
#    svn ci -m "initial commit" ./workspace/$DOCNAME
#    rm -rf ./workspace/* ./workspace/.svn




 

