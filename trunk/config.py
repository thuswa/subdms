#!/usr/bin/env python
# $Id$
# Last modified Sun Feb 22 22:07:54 2009 on violator
# update count: 11
# -*- coding:  utf-8 -*-

import ConfigParser
#import string

class dmsconfig:
    config = ConfigParser.ConfigParser()
    
    # Read 
    config.read("subdmsrc")

    # print summary
    def __init__(self):
        self.repopath = config.get("Path", "repository")
        self.doctypes = config.get("Document", "type")
