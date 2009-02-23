#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 16:39:22 2009 on havoc
# update count: 29
# -*- coding:  utf-8 -*-

import os
import pysvn
import config
import createdb

conf = config.dmsconfig()
client = pysvn.Client()

# set some vars
projname="project"
nrdocs=2;

# create workspace directory
if not os.path.isdir(conf.workpath):
    os.mkdir(conf.workpath)

# create db
createdb.creatdb(conf.dbpath)

# create subversion repository
svnadmin create $REPONAME

# copy hook to repo dir
cp post-commit ./$REPONAME/hooks
chmod +x ./$REPONAME/hooks/post-commit

# create project layout and add some docs
for DOC in conf.doctypes: 
    for N in 1 nrdocs: 
	svn mkdir --parents  -m "create doc dirs" $URR/$PROJ/$DOC/000$N
	svn co $URR/$PROJ/$DOC/000$N ./workspace
	DOCNAME=$PROJNAME-$DOC-000$N".txt"
	echo "yea it is" > ./workspace/$DOCNAME
#	echo $DOCNAME
	svn add ./workspace/$DOCNAME
	svn ci -m "initial commit" ./workspace/$DOCNAME
        rm -rf ./workspace/* ./workspace/.svn
    done
done 


 

