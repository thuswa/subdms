#!/usr/bin/env python
# $Id$
# Last modified Sun Apr 19 14:25:29 2009 on violator
# update count: 340
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

import pysvn

import lowlevel
import frontend
import string

class repository:
    def __init__(self):    
        self.client = pysvn.Client()
        self.conf = lowlevel.config()
        self.cmd = lowlevel.command()
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        self.proj = frontend.project()
        
    def createrepo(self):
        """ create repsitory and layout """
        self.cmd.svncreaterepo(self.conf.repopath)
        # Create category dirs in repo
        for cat in self.conf.categories:
            self.proj.createcategory(cat)
            
        print "Create repository: "+self.conf.repopath

    def installhooks(self):
        """ Install hooks in repository """
        repohooklist=['pre-commit', 'post-commit']
        for repohook in repohooklist:
            repohookpath = self.link.const_repohookpath(repohook)

            # Copy hooks to dir in repository and set to executable
            self.cmd.copyfile(self.link.const_hookfilepath(repohook), \
                              repohookpath)
            self.cmd.setexecutable(repohookpath)
            print "Install hook: "+repohook+" ->  "+self.conf.hookspath

    def installtemplates(self):
        """ Install templates in repository """
        # Create url for template types in repo
        category = self.conf.categories[1]
        project = 'TMPL'
        description = 'Subdms Template'
        doctypes =['GEN']
        issue = '1'
        self.proj.createproject(category, project, description, doctypes)
        # Add default templates to repo
        for tmpl in self.conf.tmpltypes:
            tmplnamelist = self.link.const_docnamelist(category, project, \
                                                      doctypes[0], issue, tmpl)
            tmplfname = self.conf.gettemplate(tmpl)
            tmplpath = self.link.const_defaulttmplpath(tmplfname)
            keywords = "general, example, template"
            self.doc.adddocument(tmplpath, tmplnamelist, "default", keywords)
            self.doc.release(tmplnamelist)
            print "Install template: "+tmplfname+" -> "+self.conf.repourl 

    def walkrepoleafs(self, path, filelist):
        """ Walk the repo and operate on all files. """
        try:
            pathlist= self.client.ls(path)        
            for p in pathlist:
                ppath = p["name"]
                oldpath = path
                self.walkrepoleafs(ppath, filelist)
        except:
            filelist.append(oldpath)

    def upgraderepo():
        """ Upgrade layout in repo. """
        # Change base dir for project documents
        client.copy(self.conf.repourl+"/trunk", self.conf.repourl+"/P") 

    def upgradefilename(filelist):
        """ Upgrade document file names. """
        for name in filelist:
            splitlist=name.split('/')
            splitlist[-1] = "P-"+splitlist[-1]
            newname = string.join(splitlist, '/')
            client.move(name, newname, "Upgrade document name")
            
