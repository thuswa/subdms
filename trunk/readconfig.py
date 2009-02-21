#!/usr/bin/env python
# $Id$
# Last modified Sun Feb 22 00:13:36 2009 on violator
# update count: 10
# -*- coding:  utf-8 -*-

import ConfigParser
#import string

config = ConfigParser.ConfigParser()

# Read 
config.read("subdmsrc")

# print summary
print config.get("Path", "repository")
print config.get("Document", "type")
