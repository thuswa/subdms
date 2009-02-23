#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 00:36:00 2009 on violator
# update count: 8
# -*- coding:  utf-8 -*-

import os
import pysvn
import config

conf = config.dmsconfig()
client = pysvn.Client()

# set some vars
REPONAME="repo"
URR="file://"$PWD/$REPONAME
PROJNAME="project"
DOCTYPE="note report"
NRDOCS=2;

# create test repo
svnadmin create $REPONAME

# copy hook to repo dir
cp post-commit ./$REPONAME/hooks
chmod +x ./$REPONAME/hooks/post-commit

# create db
./createdb.py

# create temporary check-out dir
mkdir ./workspace

# create project layout and add some docs
for DOC in $DOCTYPE; 
do
    for N in 1 $NRDOCS; 
    do
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


 

