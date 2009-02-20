#!/usr/bin/env python
# $Id$
# Last modified Fri Feb 20 20:41:23 2009 on violator
# update count: 5
# -*- coding:  utf-8 -*-

import ConfigParser
import string

config = ConfigParser.ConfigParser()

# Read 
config.read("samples/sample.ini")

# print summary
config.get("book", "title"))
