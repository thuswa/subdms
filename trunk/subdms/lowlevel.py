#!/usr/bin/env python
# $Id$
# Last modified Mon Apr  6 23:42:48 2009 on violator
# update count: 265
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
import shutil
import string
import subprocess

""" Low-level classes.  """

class config:    
    def __init__(self):
        """ set built-in and user defined configs """
        conf = ConfigParser.ConfigParser()

        # Deterimine config file path dependent on which os
        if os.name == 'nt':
            conffilepath = 'c:\\Documents and Settings\\All Users\\' \
                'Application Data\\subdms\\subdms.cfg'
        if os.name == 'posix':
            conffilepath = '/etc/subdms/subdms.cfg'
        conf.read(conffilepath)
        
        self.repopath = conf.get("Path", "repository")
        self.hookspath = os.path.join(self.repopath,"hooks") 
        self.repourl = "file:///" + self.repopath.replace("\\","/")
        self.trunkurl = self.repourl + "/trunk"
        self.tmplurl = self.repourl + "/templates"
        self.workpath = conf.get("Path", "workspace")
        self.dbpath = conf.get("Path", "database")
        self.doctypes = list(conf.get("Document", "type").split())
        self.filetypes = ['pdf','tex','txt','zip']
        self.tmpltxt = conf.get("Template", "txt")
        self.tmpltex = conf.get("Template", "tex")
        self.txteditor = conf.get("Editor", "txt")
        self.texeditor = conf.get("Editor", "tex")
        self.proplist = ['title', 'status', 'svn:keywords']
        self.svnkeywords=string.join(["LastChangedDate", \
                                      "LastChangedRevision", "Id", \
                                      "Author"])
        self.tmpl = 'template'.encode("hex")
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

    def const_tmplurl(self, tmplnamelist):
        """ Construct the template file url. """
        return string.join([self.conf.tmplurl, \
                            string.join(tmplnamelist,'.')], '/')

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
   
    def rmtree(self, path):
        """ Delete directory tree recursively. """
        shutil.rmtree(path)

    def copyfile(self, frompath, topath):
        """ Copy file. """
        shutil.copyfile(frompath, topath)
       
    def svncreaterepo(self, repopath):
        """ Create subversion repository. """
        subprocess.call(['svnadmin','create', repopath])
    
################################################################################
        
class svnlook:
    def __init__(self, repo, rvn, option):
        self.cmd = command()
        self.repourl = repo
        self.revision = rvn 
        self.svn_look = "/usr/bin/svnlook"
        self.option = option
        
    def svnlookcmd(self, command, repourl, option, option2):
        """ Svn_look command. """
        lookcmd = "%s %s %s %s %s" % (self.svn_look, "%s", "%s", "%s", "%s")
        return self.cmd.command_output(lookcmd % (command, repourl, \
                                                  option, option2))

    def svnlookcmd1(self, command, option, option2):
        """ Simplified svn look command """
        return self.svnlookcmd(command, self.repourl, option, option2)

    def svnlookcmd2(self, command):
        """ Simplified svn look command """
        return self.svnlookcmd(command, self.repourl, self.option, \
                               self.revision)
    
    def getauthor(self):
        """ Get commit author. """
        return self.svnlookcmd2("author").rstrip("\n")

    def getchanged(self):
        """ Get commit change. """
        return self.svnlookcmd2("changed")

    def getdate(self):
        """ Get commit date. """
        return self.svnlookcmd2("date").rstrip("\n")

    def getdocfname(self):
        """ get document file name """
        return self.getchanged().split("/").pop().rstrip("\n").rstrip()
        
    def getlogmsg(self):
        """ Get commit log message. """
        return self.svnlookcmd2("log").rstrip("\n").rstrip()

    def getproject(self):
        """ Get project name. """
        return self.getlogmsg().split(": ")[-1]
        
    def getstatus(self, docurl):
        """ Get commit status. """
        return self.svnlookcmd1("propget", "status", docurl)

    def gettitle(self, docurl):
        """ Get commit title. """
        return self.svnlookcmd1("propget", "title", docurl)
    
