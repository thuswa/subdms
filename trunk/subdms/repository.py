#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  7 20:53:01 2010 on stalker
# update count: 604
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

import sys

# from . import lowlevel # Python 3.X
# from . import frontend # Python 3.X
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
        
    def checkrepotools(self):
        """Check if the needed repo tools exist."""
        if not self.cmd.exists(self.conf.svnadmin):
            sys.exit("Error: Can not find svnadmin command.")
        if not self.cmd.exists(self.conf.svnlook):
            sys.exit("Error: Can not find svnlook command.")

    def createrepo(self):
        """ create repsitory and layout """
        self.cmd.svncreaterepo(self.conf.repopath)            
        # Create category dirs in repo
        for cat in self.conf.categories:
            self.proj.createcategory(cat)
        print("Create repository: "+self.conf.repopath)

    def installhooks(self):
        """ Install hooks in repository """
        repohooklist=['pre-commit', 'post-commit']
        for repohook in repohooklist:
            repohookpath = self.link.const_repohookpath(repohook)

            # Copy hooks to dir in repository and set to executable
            self.cmd.copyfile(self.link.const_hookfilepath(repohook), \
                              repohookpath)
            self.cmd.setexecutable(repohookpath)
            print("Install hook: "+repohook+" ->  "+self.conf.hookspath)

    def installtemplates(self):
        """ Install templates in repository """
        doc = frontend.document()
        # Create url for template types in repo
        category = self.conf.categories[1]
        project = "TMPL"
        description = 'Subdms Template'
        defaulttype = "GEN"
        doctypes = [defaulttype]
        doctypes.extend(self.conf.doctypes.split(","))
        issue = '1'
        # Create template project
        self.proj.createproject(category, project, description, doctypes)
        # Add default templates to repo
        for tmpl in self.conf.tmpltypes:
            tmplnamelist = self.link.const_docnamelist(category, project, \
                                                   defaulttype, issue, tmpl)
            tmplfname = self.conf.gettemplate(tmpl)
            tmplpath = self.link.const_defaulttmplpath(tmplfname)
            keywords = "general, example, template"
            doc.adddocument(tmplpath, tmplnamelist, "default", keywords)
            doc.release(tmplnamelist)
            print("Install template: "+tmplfname+" -> "+self.conf.repourl) 

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
            if p["kind"] == self.svncmd.filekind:
                filenamelist.append(p["name"])
        return filenamelist   

    def walkreponodes(self, path):
        """ Walk the repo and list all paths. """
        pathnamelist = []
        for p in self.svncmd.recursivels(path):
            if p["kind"] != self.svncmd.filekind:
                pathnamelist.append(p["name"])
        return pathnamelist   

    def upgraderepo(self):
        """ Upgrade layout in repo. """
        projpath = self.conf.repourl+"/P"
        trunkpath = self.conf.repourl+"/trunk"
        splitpath = trunkpath.rsplit("///")[1]

        # Create category dirs in repo
        for cat in self.conf.categories:
            self.proj.createcategory(cat)
        
        for old_path in self.walkreponodes(trunkpath):
            new_path = projpath + old_path.rsplit(splitpath)[1].upper()
            print(new_path)
            self.svncmd.mkdir(new_path, "Upgrade document path")

    def upgradefilename(self):
        """ Upgrade document file names. """
        projpath = self.conf.repourl+"/P"
        trunkpath = self.conf.repourl+"/trunk"
        splitpath = trunkpath.rsplit("///")[1]
                
        for old_name in self.walkrepoleafs(trunkpath):
            docext = old_name.rsplit(".")[1]
            new_base = old_name.rsplit(splitpath)[1].rsplit(".")[0].upper()
            new_baselist = new_base.split("/")
            new_basename = "P-" + new_baselist[-1]             
            new_path = string.join(new_baselist[:-1], "/")
            new_name = projpath + new_path + "/" + new_basename + \
                       "." + docext
            print(new_name)
            self.svncmd.server_side_copy(old_name, new_name, \
                                               "Upgrade document name")
            
