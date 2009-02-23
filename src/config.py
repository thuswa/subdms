#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 14:45:48 2009 on havoc
# update count: 28
# -*- coding:  utf-8 -*-

import ConfigParser

class dmsconfig:
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("../subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.repourl = "file://" + self.repopath
        self.workpath = conf.get("Path", "workspace")
        self.doctypes = list(conf.get("Document", "type").split())
