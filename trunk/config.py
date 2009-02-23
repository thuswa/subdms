#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 00:38:15 2009 on violator
# update count: 27
# -*- coding:  utf-8 -*-

import ConfigParser

class dmsconfig:
    
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("subdms.cfg")
        
        self.repopath = conf.get("Path", "repository")
        self.repourl = "file://" + self.repopath
        self.workpath = conf.get("Path", "workspace")
        self.doctypes = list(conf.get("Document", "type").split())
