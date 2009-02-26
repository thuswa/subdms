#!/usr/bin/env python
# $Id$
# Last modified Thu Feb 26 13:21:22 2009 on havoc
# update count: 30
# -*- coding:  utf-8 -*-

import ConfigParser

class dmsconfig:
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("../subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.repourl = "file://" + self.repopath
        self.workpath = conf.get("Path", "workspace")
        self.dbpath = conf.get("Path", "database")
        self.tmplpath = conf.get("Path", "template")
        self.doctypes = list(conf.get("Document", "type").split())
