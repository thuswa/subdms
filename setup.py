#!/usr/bin/env python
# $Id$
# Last modified Fri Mar 13 14:12:37 2009 on havoc
# update count: 39

from distutils.core import setup

setup(name='subdms',
      version='0.0.1',
      description='',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPL',
      long_description = """
      """,
      url='http://subdms.googlecode.com',
      packages=[''],
      package_dir = {'' : '' },
      platforms='any',
      requires=['pysvn', 'pyqt4', 'sqlite3', 'svn']
      )
