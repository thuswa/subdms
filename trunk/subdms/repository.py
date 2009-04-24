#!/usr/bin/env python
# $Id$
# Last modified Fri Apr 24 14:46:38 2009 on violator
# update count: 474
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

import lowlevel
import frontend
import string

class repository:
    def __init__(self):    
        self.conf = lowlevel.config()
        self.cmd = lowlevel.command()
        self.link = lowlevel.linkname()
        self.proj = frontend.project()
        self.svncmd = lowlevel.svncmd()
        
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
        doc = frontend.document()
        # Create url for template types in repo
        category = self.conf.categories[1]
        project = "TMPL"
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
            doc.adddocument(tmplpath, tmplnamelist, "default", keywords)
            doc.release(tmplnamelist)
            print "Install template: "+tmplfname+" -> "+self.conf.repourl 

    def walkrepo(self, path):
        """ Walk the repo and list the content. """
        repolist= []
        for p in self.svncmd.recursivels(path):
            repolist.append(p["name"])
        return repolist   

    def walkrepoleafs(self, path):
        """ Walk the repo and list all files. """
        filenamelist= []
        for p in self.svncmd.recursivels(path):
            if p["kind"] == pysvn.node_kind.file:
                filenamelist.append(p["name"])
        return filenamelist   

    def walkreponodes(self, path):
        """ Walk the repo aand list all paths. """
        pathnamelist = []
        for p in self.svncmd.recursivels(path):
            if p["kind"] != pysvn.node_kind.file:
                pathnamelist.append(p["name"])
        return pathnamelist   

    def upgraderepo(self):
        """ Upgrade layout in repo. """
        # Change base dir for project documents        
        self.svncmd.server_side_copy(self.conf.repourl+"/trunk", \
                                  self.conf.repourl+"/P", \
                                  "Upgrade repo layout") 
        for path in self.walkreponodes(self.conf.repourl+"/P"):
            self.svncmd.server_side_move(path, path.upper(), \
                                               "Upgrade document path")

    def upgradefilename(self):
        """ Upgrade document file names. """
        for name in self.walkrepleafs(self.conf.repourl+"/P"):
            self.svncmd.server_side_move(name, name.upper(), \
                                               "Upgrade document name")
            
