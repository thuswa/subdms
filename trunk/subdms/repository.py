#!/usr/bin/env python
# $Id$
# Last modified Mon Apr  6 23:36:38 2009 on violator
# update count: 189
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
import string

import lowlevel

class repository:
    def __init__(self):    
        self.client = pysvn.Client()
        self.conf = lowlevel.config()
        self.cmd = lowlevel.command()

    def createrepo(self):
        """ create repsitory and layout """
        self.cmd.svncreaterepo(self.conf.repopath)
        self.client.mkdir(self.conf.trunkurl, "create trunk directory",1)
        self.client.mkdir(self.conf.tmplurl, "create templates directory",1)
        print "Create repository: "+self.conf.repopath

    def installhooks(self):
        """ Install hooks in repository """
        revhooklist=['pre-commit', 'post-commit']
        for revhook in revhooklist:
            revhookpath=os.path.join(self.conf.hookspath, revhook)
            # Copy hooks to dir in repository and set to executable
            self.cmd.copyfile(os.path.join(self.conf.pkgpath, revhook+'.py'), \
                              revhookpath) #fixme
            os.chmod(revhookpath,0755)
            print "Install hook: "+revhook+" ->  "+self.conf.hookspath

    def installtemplates(self):
        """ Install templates in repository """
        tmpldir=os.path.join(self.conf.workpath,'templates')
        txtfiledir=os.path.join(tmpldir, self.conf.tmpltxt)
        texfiledir=os.path.join(tmpldir, self.conf.tmpltex)
        txtfilepath=os.path.join(self.conf.tmplpath, self.conf.tmpltxt)
        texfilepath=os.path.join(self.conf.tmplpath, self.conf.tmpltex)
        
        # Check out templates dir
        self.client.checkout(self.conf.tmplurl, tmpldir)
        
        # Add templates to dir
        self.cmd.copyfile(txtfilepath, txtfiledir)
        self.cmd.copyfile(texfilepath, texfiledir)
        self.client.add(txtfiledir)
        self.client.add(texfiledir)
        self.client.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                            txtfiledir)
        self.client.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                            texfiledir)
        
        # Commit templates
        self.client.checkin(txtfiledir, self.conf.tmpl+\
                            "installing default txt template")
        self.client.checkin(texfiledir, self.conf.tmpl+\
                            "installing default tex template")
        print "Install template: "+self.conf.tmpltxt+" -> "+self.conf.tmplurl 
        print "Install template: "+self.conf.tmpltex+" -> "+self.conf.tmplurl 

        # Remove template dir from workspace
        self.cmd.rmtree(tmpldir)


