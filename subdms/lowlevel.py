#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Sat Aug  1 20:16:03 2009 on violator
# update count: 691
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
import pysvn
import shutil
import string
import subprocess
#import win32api
#import win32con

import database

""" Low-level classes. """

class config:    
    def __init__(self):
        """ set built-in and user defined configs """
        self.conf = ConfigParser.ConfigParser()

        # Determine config file path dependent on which os
        if os.name == 'nt':
            conffilepath = 'c:\\Documents and Settings\\All Users\\' \
                'Application Data\\subdms\\subdms.cfg'
        if os.name == 'posix':
            conffilepath = '/etc/subdms/subdms.cfg'
        self.conf.read(conffilepath)

        # Package paths
        self.pkgpath = os.path.dirname(os.path.realpath(__file__))
        self.tmplpath = os.path.join(self.pkgpath, "templates")
        self.iconpath = os.path.join(self.pkgpath, "icons")
        self.helppath = os.path.join(self.pkgpath, "docs/README.html")
        #/usr/share/icons/oxygen/22x22/actions/go-

        # DMS paths
        self.repopath = self.conf.get("Path", "repository")
        self.hookspath = os.path.join(self.repopath,"hooks") 
        self.repourl = "file:///" + self.repopath.replace("\\","/")
        self.workpath = self.conf.get("Path", "workspace")
        self.dbpath = self.conf.get("Path", "database")
        self.doctypes = self.conf.get("Document", "type").replace(" ",",")

        self.userfiletypes = self.conf.get("User Defined", "filetypes")
        self.svnlook = self.conf.get("Cmd", "svnlook")
        self.svnadmin = self.conf.get("Cmd", "svnadmin")

        # DMS Lists
        self.categories = ['P','T']
        self.filetypes = ['odp','ods','odt','pdf','tex','txt','zip']
        self.tmpltypes = ['odt','tex','txt']
        self.odftypes = ['odp','ods,','odt']
        self.integtypes = ['odp','ods,','odt','tex']
        self.proplist = ['title', 'status', 'svn:keywords', 'keywords']
        self.statuslist = ['preliminary', 'in-review' ,'rejected', 'approved', \
                           'released', 'obsolete'] 
        self.svnkeywords=string.join(["LastChangedDate", \
                                      "LastChangedRevision", "Id", \
                                      "Author"])
        self.fields = ['subdmsauthor', 'subdmsdocid', 'subdmsissue', \
                       'subdmskeyw', 'subdmsproj', 'subdmsrdate', \
                       'subdmsstatus', 'subdmstitle']

        self.odfcontent = "content.xml"

        self.vc = ['view', 'copy']
        self.ro = ['read', 'only']

        # Internal Trigger patterns
        self.statchg = 'statuschange'.encode("hex")
        self.newdoc = 'newdocument'.encode("hex")
        self.newdoctype = 'newdoctype'.encode("hex")
        self.newproj = 'newproject'.encode("hex")
        self.newtitle = 'newtitle'.encode("hex")
        self.newkeywords = 'newkeywords'.encode("hex")
        self.release = 'release'.encode("hex")
        self.obsolete = 'obsolete'.encode("hex")

    def isodf(self, docnamelist):
        """ Is a odf file. """
        if docnamelist[-1] in self.odftypes: 
            return True
        else:
            return False

    def istex(self, docnamelist):
        """ Is a tex file. """
        if docnamelist[-1] == "tex": 
            return True
        else:
            return False
        
    def geteditor(self, filetype):
        """ Get appropriate editor for filetype. """
        try:
            editor = self.conf.get("Editor", filetype)
        except:
            editor = self.conf.get("Editor", "default")
        finally:
            return editor
    
    def gettemplate(self, tmpltype):
        """ Get default template. """
        tmpls = {'odt' : 'default.odt', 'txt' : 'default.txt', \
                 'tex' : 'default.tex' }
        return tmpls[tmpltype]

    def getfilefilter(self):
        """ Get file filter for file dialog. """
        # define filter strings
        usrfilterstr = self.userfiletypes 
        stdfilterstr = "Open Document Format (.odp, .ods, .odt)" \
                       "(*.odp *.ods *.odt);;" \
                       "Text (.txt, .tex) (*.txt *.tex);;" \
                       "Portable Document Format (pdf) (*.pdf);;" \
                       "Compressed (zip) (*.zip);;"

        # if no user defined file types return standard filter string
        if not usrfilterstr:
            return stdfilterstr
        else:
            usrdisp = "." + usrfilterstr.replace(" "," .")
            usrfilter = "*" + usrdisp.replace(" "," *")
            return stdfilterstr + "User Defined (%s) (%s);;" % \
                   (usrdisp, usrfilter)

    def getsupportedfiletypes(self):
        """ define the supported fileypes."""
        returnlist = self.filetypes
        if self.userfiletypes:
           returnlist.extend(self.userfiletypes.split(" ")) 
        return returnlist

################################################################################

class linkname:
    def __init__(self):    
        self.conf = config()
        
    def const_checkoutpath(self, docnamelist):
        """ Construct the check-out path """
        return os.path.join(self.conf.workpath, \
                        os.path.splitext(self.const_docname(docnamelist))[0])

    def const_readonlypath(self, docnamelist):
        """ Construct the read-only path """
        doclist=docnamelist[:-1]
        doclist.extend(self.conf.ro)
        doclist.extend(docnamelist[-1:])
        return os.path.join(self.conf.workpath, self.const_docname(doclist))

    def const_readonlyfilepath(self, docnamelist):
        """ Construct the read-only path """
        return os.path.join(self.const_readonlypath(docnamelist), \
                            self.const_docfname(docnamelist))

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
        docurllist=[self.conf.repourl]
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

    def const_doctmppath(self, docnamelist):
        """ Construct the path to the tmp document. """
        tmplist = docnamelist[:]
        tmplist[-1]= 'tmp'
        return os.path.join(self.const_checkoutpath(tmplist), \
                                self.const_docfname(tmplist))

    def const_caturl(self, category):
        """ Construct the category url. """
        return string.join([self.conf.repourl, category], "/")

    def const_projurl(self, category, project):
        """ Construct the project url. """
        return string.join([self.const_caturl(category), project], "/")
    
    def const_doctypeurl(self, category, project, doctype):
        """ Construct the document type url. """
        return string.join([self.const_projurl(category, project), doctype], \
                           "/")

    def const_docnamelist(self, category, project, doctype, issue, docext):
        """
        Create docnamelist - list containing the building blocks of
        the document name
        """
        db = database.sqlitedb()
        docno="%04d" % (db.getdocno(category, project, doctype) + 1)
        return [category, project, doctype, docno, issue, docext]
  
    def deconst_docfname(self, docname):
        """ De-construct document file name. """
        return list(docname.replace(".","-").split("-"))  

    def const_defaulttmplpath(self, tmplname):
        """ Construct the default template file path. """
        return os.path.join(self.conf.tmplpath, tmplname)

    def const_repohookpath(self, repohook):
        """ Construct repository hook path. """
        return os.path.join(self.conf.hookspath, repohook)

    def const_hookfilepath(self, hookfile):
        """ Construct path to hook file. """
        return os.path.join(self.conf.pkgpath, hookfile+'.py')

################################################################################

class command:
    def __init__(self):
        """ Initialize command class """
        self.conf = config()
        self.link = linkname()
    
    def command_output(self, cmd):
        """ Capture a command's standard output. """
        
        return subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE).communicate()[0]

    def copyfile(self, frompath, topath):
        """ Copy file. """
        shutil.copyfile(frompath, topath)

    def movefile(self, frompath, topath):
        """ Move file. """
        shutil.move(frompath, topath)

    def renamefile(self, frompath, topath):
        """ Rename file. """
        os.rename(frompath, topath)

    def exists(self, path):
        """ Check if path exists. """
        return os.path.exists(path)

    def whereis(self, program):
        """ Check program location. """
        for path in os.environ.get('PATH', '').split(':'):
            if os.path.exists(os.path.join(path, program)) and \
                    not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
            return None        

    def rm(self, path):
        """ Delete file. """
        os.remove(path)

    def rmtree(self, path):
        """ Delete directory tree recursively. """
        shutil.rmtree(path)

        #    def rmtree(self, path):
#        """
#        Delete directory tree recursively.
#        Windows OS version, checks if file is read-only 
#        """
#        retry = True
#        while retry:
#            retry = False
#            try:
#                shutil.rmtree(path)
#            except exceptions.WindowsError, e:
#                if e.winerror == 5: # No write permission
#                    win32api.SetFileAttributes(path, \
#                                               win32con.FILE_ATTRIBUTE_NORMAL)
#                    retry = True

    def setreadonly(self, filepath):
        """ Set file to read-only. """
        os.chmod(filepath, 0444)

    def setexecutable(self, filepath):
        """ Set file to executable. """
        os.chmod(filepath, 0755)

    def launch_editor(self, docnamelist):
        """ Launch appropriate editor. """
        docpath = self.link.const_docpath(docnamelist)
        filetype = docnamelist[-1]
        os.system("%s %s &" % (self.conf.geteditor(filetype), docpath))

    def launch_viewer(self, docnamelist):
        """ Launch appropriate viewer. """
        docpath = self.link.const_readonlyfilepath(docnamelist)
        filetype = docnamelist[-1]
        os.system("%s %s &" % (self.conf.geteditor(filetype), docpath))

    def workingcopyexists(self, docnamelist):
        """ Check if working copy exists. """
        return self.exists(os.path.join( \
            self.link.const_checkoutpath(docnamelist), '.svn'))

    def repoexists(self):
        """ Check if repo exists. """
        return self.exists(self.conf.repopath)

    def dbexists(self):
        """ Check if database exists. """
        return self.exists(self.conf.dbpath)

    def createworkspace(self):
        """ Create workspace directory. """
        if not os.path.isdir(self.conf.workpath):
            os.makedirs(self.conf.workpath)
            print "Create workspace: "+ self.conf.workpath

    def createdbpath(self):
        """ Create database directory. """
        dbbasedir = os.path.dirname(self.conf.dbpath)
        if not os.path.isdir(dbbasedir):
            os.makedirs(dbbasedir)
    
    def svncreaterepo(self, repopath):
        """ Create subversion repository. """
        repobasedir = os.path.dirname(self.conf.repopath)
        if not os.path.isdir(repobasedir):
            os.makedirs(repobasedir)
        subprocess.call([self.conf.svnadmin,'create', repopath])

################################################################################
        
class svnlook:
    def __init__(self, svnlook, repo, rvn, option):
        self.cmd = command()
        self.repourl = repo
        self.revision = rvn 
        self.svn_look = svnlook
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

    def getcategory(self):
        """ Get project acronym. """
        return self.getchanged().split(" ")[3].split("/")[0]

    def getproject(self):
        """ Get project acronym. """
        return self.getchanged().split(" ")[3].split("/")[1]

    def getdoctype(self):
        """ Get document type. """
        return self.getchanged().split(" ")[3].split("/")[2]
    
    def getstatus(self, docurl):
        """ Get commit status. """
        return self.svnlookcmd1("propget", "status", docurl)

    def gettitle(self, docurl):
        """ Get commit title. """
        return self.svnlookcmd1("propget", "title", docurl)
    
    def getkeywords(self, docurl):
        """ Get commit keywords. """
        return self.svnlookcmd1("propget", "keywords", docurl)

################################################################################

class svncmd:
    def __init__(self):
        """ Initialize subversion command class """
        self.client = pysvn.Client()
        self.modified = pysvn.wc_status_kind.modified
        self.conflicted = pysvn.wc_status_kind.conflicted
        self.filekind = pysvn.node_kind.file
        
    def add(self, path):
        """ Add to repository. """
        self.client.add(path)
        
    def checkin(self, path, log_message):
        """ Check-out from repo. """
        self.client.checkin(path, log_message)
        
    def checkout(self, url, path):
        """ Check-out from repo. """
        self.client.checkout(url, path)

    def export(self, url, path):
        """ Export form repository. """
        self.client.export(url, path, True)

    def info(self, path):
        """ return repository info. """
        return self.client.info(path)
    
    def mkdir(self, url, log_message):
        """ Make directory in repository. """  
        self.client.mkdir(url, log_message, 1)
        
    def propget(self, property,  url):
        """ Get property. """
        return self.client.propget(property, url).values().pop()

    def propset(self, property, propvalue, path):
        """ Set property. """
        self.client.propset(property, propvalue, path)

    def revert(self, path):
        """ Discard any changes in the working copy at path. """
        self.client.revert(path)

    def recursivels(self, path):
        """ Return resursive listing of repourl. """ 
        return self.client.ls(path, \
                              pysvn.Revision(pysvn.opt_revision_kind.head),
                              True)

    def server_side_copy(self, source, target, log_message):
        """ Server side copy in repository URL -> URL. """
        def get_log_message():
            return True, log_message
        self.client.callback_get_log_message = get_log_message
        self.client.copy(source, target)

    def server_side_move(self, source, target, log_message):
        """ Server side move in repository URL -> URL. """
        def get_log_message():
            return True, log_message
        self.client.callback_get_log_message = get_log_message
        self.client.move(source, target)

    def status(self, path):
        """ Return status of working copy file. """
        return self.client.status(path)[0]

