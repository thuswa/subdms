#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 22:21:27 2009 on violator
# update count: 137
# -*- coding:  utf-8 -*-
#
# subdms - A document management system based on subversion.
# Copyright (C) 2009  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


