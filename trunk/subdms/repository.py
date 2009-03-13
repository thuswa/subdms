#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 00:46:07 2009 on violator
# update count: 135
# -*- coding:  utf-8 -*-

import os
import pysvn
import shutil
import string
import subprocess 

import lowlevel

class repository:
    def __init__(self):    
        self.client = pysvn.Client()
        self.conf = lowlevel.config()
        
    def createrepo(self):
        """ create repsitory and layout """
        subprocess.call(['svnadmin','create', self.conf.repopath])
        self.client.mkdir(self.conf.trunkurl, "create trunk directory",1)
        self.client.mkdir(self.conf.tagsurl, "create trunk directory",1)
        self.client.mkdir(self.conf.tmplurl, "create templates directory",1)

    def installhooks(self):
        """ Install hooks in repository """
        revhook='post-commit'
        revhookpath=os.path.join(self.conf.hookspath, revhook)
        # Copy hooks to dir in repository and set to executable
        shutil.copyfile(os.path.abspath(revhook), revhookpath)
        os.chmod(revhookpath,0755)
        
    def installtemplates(self):
        """ Install templates in repository """
        tmplpath=os.path.join(self.conf.workpath,'templates')
        txtfilepath=os.path.join(tmplpath, self.conf.tmpltxt.split('/')[1])
        #fixme
        
        # Check out templates dir
        self.client.checkout(self.conf.tmplurl, tmplpath)
        
        # Add templates to dir
        shutil.copyfile(os.path.abspath(self.conf.tmpltxt), txtfilepath)
        self.client.add(txtfilepath)

        # Commit templates
        self.client.checkin(tmplpath, "installing templates")
   
        # Remove template dir from workspace
        shutil.rmtree(tmplpath)


