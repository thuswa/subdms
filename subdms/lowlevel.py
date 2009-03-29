#!/usr/bin/env python
# $Id$
# Last modified Sun Mar 29 12:50:24 2009 on violator
# update count: 166
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

import ConfigParser
import os
import string
import subprocess

""" Low-level classes.  """

class config:    
    def __init__(self):
        """ set built-in and user defined configs """
        conf = ConfigParser.ConfigParser()
        conf.read("/etc/subdms/subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.hookspath = os.path.join(self.repopath,"hooks") 
        self.repourl = "file://" + self.repopath
        self.trunkurl = self.repourl + "/trunk"
        self.tmplurl = self.repourl + "/templates"
        self.workpath = conf.get("Path", "workspace")
        self.dbpath = conf.get("Path", "database")
        self.doctypes = list(conf.get("Document", "type").split())
        self.filetypes = ['txt','tex']
        self.tmpltxt = conf.get("Template", "txt")
        self.tmpltex = conf.get("Template", "tex")
        self.txteditor = conf.get("Editor", "txt")
        self.texeditor = conf.get("Editor", "tex")
        self.proplist = ['title', 'status', 'svn:keywords']
        self.svnkeywords=string.join(["LastChangedDate", \
                                      "LastChangedRevision", "Id", \
                                      "Author"])
        self.statchg = 'statuschange'.encode("hex")
        self.newdoc = 'newdocument'.encode("hex")
        self.newproj = 'newproject'.encode("hex")
        self.release = 'release'.encode("hex")
        self.obsolete = 'obsolete'.encode("hex")
        self.statuslist = ['preliminary', 'in-review' ,'rejected', 'approved', \
                           'released', 'obsolete'] 
        self.pkgpath = os.path.dirname(os.path.realpath(__file__))
        self.tmplpath = os.path.join(self.pkgpath, "templates")
        
################################################################################

class docname:
    def __init__(self):    
        self.conf = config()

    def const_checkoutpath(self, docnamelist):
        """ Construct the check-out path """
        return os.path.join(self.conf.workpath, \
                        os.path.splitext(self.const_docname(docnamelist))[0])

    def const_docname(self, docnamelist):
        """ Construct the document name. """
        return string.join(docnamelist[:-1],'-')

    def const_docid(self, docnamelist):
        """ Construct the document name. """
        return string.join(docnamelist[:-2],'-')

    def const_docfname(self, docnamelist):
        """ Construct the document file name. """
        return self.const_docname(docnamelist)+'.'+docnamelist[-1:].pop()

    def const_docurl(self, docnamelist):
        """ Construct the document url. """
        docurllist=[self.conf.trunkurl]
        docurllist.extend(docnamelist[:-1])
        return string.join(docurllist, '/')

    def const_docfileurl(self, docnamelist):
        """ Construct the document file url. """
        return string.join([self.const_docurl(docnamelist), \
                                self.const_docfname(docnamelist)], '/')

    def const_docinrepopath(self, docnamelist):
        """ Construct the document file path in repository. """
        return self.const_docfileurl(docnamelist).split(self.conf.repopath)[1]
 
    def const_docpath(self, docnamelist):
        """ Construct the path to the checked out document. """
        return os.path.join(self.const_checkoutpath(docnamelist), \
                                self.const_docfname(docnamelist))

    def deconst_docfname(self, docname):
        """ De-construct document file name. """
        return list(docname.replace(".","-").split("-"))  

################################################################################

class command:
    def __init__(self):
        self.conf = config()
        
    def command_output(self, cmd):
        " Capture a command's standard output. "
        return subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE).communicate()[0]

    def launch_editor(self, docpath):
        " Launch appropriate editor. "
        os.system("%s %s &" % (self.conf.txteditor, docpath))
