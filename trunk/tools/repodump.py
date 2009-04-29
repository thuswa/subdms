#!/usr/bin/env python
# $Id$
# Last modified Wed Apr 29 14:24:57 2009 on violator
# update count: 136
# -*- coding:  utf-8 -*-

from subdms import lowlevel

svncmd = lowlevel.svncmd()
conf = lowlevel.config()

# Dump database
print svncmd.recursivels(conf.repourl)


