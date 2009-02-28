#!/usr/bin/env python
# $Id$
# Last modified Sat Feb 28 23:01:25 2009 on violator
# update count: 33
# -*- coding:  utf-8 -*-

import ConfigParser

class dmsconfig:
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("../subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.repourl = "file://" + self.repopath
        self.trunkurl = self.repourl + "/trunk"
        self.tagsurl = self.repourl + "/tags"
        self.tmplurl = self.repourl + "/templates"
        self.workpath = conf.get("Path", "workspace")
        self.dbpath = conf.get("Path", "database")
        self.doctypes = list(conf.get("Document", "type").split())
        self.tmpltxt = conf.get("Template", "txt")
        
