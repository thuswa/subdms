#!/usr/bin/env python
# $Id$
# Last modified Thu Apr  9 00:49:38 2009 on violator
# update count: 255
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
        self.link = lowlevel.linkname()

    def createrepo(self):
        """ create repsitory and layout """
        self.cmd.svncreaterepo(self.conf.repopath)
        self.client.mkdir(self.conf.trunkurl, "create trunk directory",1)
        print "Create repository: "+self.conf.repopath

    def installhooks(self):
        """ Install hooks in repository """
        revhooklist=['pre-commit', 'post-commit']
        for revhook in revhooklist:
            revhookpath=os.path.join(self.conf.hookspath, revhook)
            # Copy hooks to dir in repository and set to executable
            self.cmd.copyfile(os.path.join(self.conf.pkgpath, revhook+'.py'), \
                              revhookpath) #fixme
            self.cmd.setexecutable(revhookpath)
            print "Install hook: "+revhook+" ->  "+self.conf.hookspath

    def installtemplates(self):
        """ Install templates in repository """
        # Create url for template types in repo
        self.createtmplurls()

        # Add default templates to repo
        for tmpl in self.conf.tmpltypes:
            tmplfname = self.conf.gettemplate(tmpl)
            tmplnamelist = self.link.deconst_tmplfname(tmplfname)
            tmplpath = self.link.const_defaulttmplpath(tmplfname)
            self.addtemplate(tmplpath, tmplnamelist)                
            print "Install template: "+tmplfname+" -> "+self.conf.tmplurl 

    def addtemplate(self, addtemplatepath, tmplnamelist):
        """ Add new template to repo. """
        tmplfname = self.link.const_tmplfname(tmplnamelist)
        tmplurl = self.link.const_tmplurl(tmplnamelist)
        tmpldir = self.link.const_tmpldir(tmplnamelist)
        tmplfilepath = self.link.const_tmplfilepath(tmplnamelist)

        # Create template url in repository and check it out to workspace
        self.client.mkdir(tmplurl, "create directory for template: "+ \
                          tmplfname,1)
        self.client.checkout(tmplurl, tmpldir)

        # Add templates to dir
        self.cmd.copyfile(addtemplatepath, tmplfilepath)
        self.client.add(tmplfilepath)

        self.client.propset(self.conf.proplist[2], self.conf.svnkeywords, \
                            tmplfilepath)
        
        # Commit templates
        self.client.checkin(tmplfilepath, self.conf.tmpl+\
                            "Installing template: "+tmplfname)

        # Remove template dir from workspace
        self.cmd.rmtree(tmpldir)

    def createtmplurls(self):
        """ Create template file type urls. """
        for tmpl in self.conf.tmpltypes:
            self.client.mkdir(self.link.const_tmpltypeurl(tmpl), \
                              "Create directory for template file type: "\
                              +tmpl,1)

