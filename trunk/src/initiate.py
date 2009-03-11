#!/usr/bin/env python
# $Id$
# Last modified Wed Mar 11 01:02:52 2009 on violator
# update count: 116
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil
import string
import subprocess 

import config
import database


class repository:
    def __init__(self):    
        self.client = pysvn.Client()

    def createrepo(self):
        """ create repsitory and layout """
        subprocess.call(['svnadmin','create',conf.repopath])
        self.client.mkdir(conf.trunkurl, "create trunk directory",1)
        self.client.mkdir(conf.tagsurl, "create trunk directory",1)
        self.client.mkdir(conf.tmplurl, "create templates directory",1)

    def installhooks(self):
        """ Install hooks in repository """
        revhook='post-commit'
        revhookpath=os.path.join(conf.hookspath, revhook)
        # Copy hooks to dir in repository and set to executable
        shutil.copyfile(os.path.abspath('lowlib.py'), \
                        os.path.join(conf.hookspath, 'lowlib.py')) #fixme
        shutil.copyfile(os.path.abspath('../subdms.cfg'), \
                        os.path.join(conf.repopath, 'subdms.cfg')) #fixme
        shutil.copyfile(os.path.abspath(revhook), revhookpath)
        os.chmod(revhookpath,0755)
        
    def installtemplates(self):
        """ Install templates in repository """
        tmplpath=os.path.join(conf.workpath,'templates')
        txtfilepath=os.path.join(tmplpath, conf.tmpltxt.split('/')[1]) #fixme
        
        # Check out templates dir
        self.client.checkout(conf.tmplurl, tmplpath)
        
        # Add templates to dir
        shutil.copyfile(os.path.abspath(conf.tmpltxt), txtfilepath)
        self.client.add(txtfilepath)

        # Commit templates
        self.client.checkin(tmplpath, "installing templates")
   
        # Remove template dir from workspace
        shutil.rmtree(tmplpath)

conf = config.dmsconfig()
repo = repository()

# create workspace directory
if not os.path.isdir(conf.workpath):
    os.makedirs(conf.workpath)

# create db
db = database.sqlitedb(conf.dbpath)
db.createdb()

# create subversion repository and layout
repo.createrepo()

# install templates
repo.installtemplates()

# install hooks
repo.installhooks()

