#!/usr/bin/env python
# $Id$
# Last modified Sun Mar 15 00:55:25 2009 on violator
# update count: 94
# -*- coding:  utf-8 -*-
#
# subdms - A document management system based on subversion.
# Copyright (C) 2009  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

import shutil
import string
import sys

CLASSIFIERS = [
    'Development Status :: 1 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX',
    'Programming Language :: Python'
    'Topic :: Desktop Environment :: Qt',
    'Topic :: Office/Business :: Document Management',
]

setup(name='subdms',
      version='0.0.1',
      description='A document management system based on subversion',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      classifiers= CLASSIFIERS,
      license='GPL',
      long_description = """
      """,
      url='http://subdms.googlecode.com',
      packages=['subdms'],
      package_data = {'subdms' : ['templates/*'] },
      data_files = [('/etc/subdms', ['subdms.cfg'])],
      scripts = ['subdms/subdms', 'subdms/subdms-server'],
      platforms='any',
      requires=['pysvn', 'pyqt4', 'pysqlite3', 'svn']
      )