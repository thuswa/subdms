#!/usr/bin/env python
# $Id$
# Last modified Sun Mar  8 23:49:33 2009 on violator
# update count: 57
# -*- coding:  utf-8 -*-

import ConfigParser

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
