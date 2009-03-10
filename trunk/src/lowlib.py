#!/usr/bin/env python
# $Id$
# Last modified Tue Mar 10 17:13:22 2009 on havoc
# update count: 89
# -*- coding:  utf-8 -*-

import ConfigParser
import os
import string

""" Low-evel classes.  """

class dmsconfig:
    
    def __init__(self):
        """ set built-in and user defined configs """
        conf = ConfigParser.ConfigParser()
        conf.read("../subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.hookspath = self.repopath + "/hooks" 
        self.repourl = "file://" + self.repopath
        self.trunkurl = self.repourl + "/trunk"
        self.tagsurl = self.repourl + "/tags"
        self.tmplurl = self.repourl + "/templates"
        self.workpath = conf.get("Path", "workspace")
        self.dbpath = conf.get("Path", "database")
        self.doctypes = list(conf.get("Document", "type").split())
        self.tmpltxt = conf.get("Template", "txt")
        self.proplist = ['title', 'issue', 'status']
        self.created = 'created'.encode("hex")
        self.statuslist = ['preliminary', 'in-review' ,'rejected', 'approved', \
                           'released', 'obsolete'] 

################################################################################

class docname:
    def __init__(self):    
        self.conf = dmsconfig()

    def const_checkoutpath(self, docnamelist):
        """ Construct the check-out path """
        return os.path.join(self.conf.workpath, \
                                os.path.splitext(self.const_docname(docnamelist))[0])

    def const_docname(self, docnamelist):
        """ Construct the document file name. """
        return string.join(docnamelist[:-1],'-')+'.'+docnamelist[-1:].pop()

    def const_docurl(self, docnamelist):
        """ Construct the document url. """
        docurllist=[self.conf.trunkurl]
        docurllist.extend(docnamelist[:-1])
        return string.join(docurllist, '/')

    def const_docfileurl(self, docnamelist):
        """ Construct the document file url. """
        return string.join([self.const_docurl(docnamelist), \
                                self.const_docname(docnamelist)], '/')

    def const_doctagurl(self, docnamelist, issue_no):
        """ Construct the document tag url. """
        docurllist=[self.conf.tagsurl]
        docurllist.extend(docnamelist[:-1])
        docurllist.extend(issueno)
        return string.join(docurllist, '/')

    def const_docpath(self, docnamelist):
        """ Construct the path to the checked out document. """
        return os.path.join(self.const_checkoutpath(docnamelist), \
                                self.const_docname(docnamelist))

    def decons_docname(self, docname):
        """ De-construct document file name. """
        return list(docname.replace(".","-").split("-"))  
