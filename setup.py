#!/usr/bin/env python
# $Id$
# Last modified Fri Mar 13 22:07:38 2009 on violator
# update count: 57

from distutils.core import setup

setup(name='subdms',
      version='0.0.1',
      description='A document management system (DMS) based on subversion',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPL',
      long_description = """
      """,
      url='http://subdms.googlecode.com',
      packages=['subdms'],
#      package_data = {'' : './subdms.cfg' },
#      scripts = ['subdms']
      platforms='any',
      requires=['pysvn', 'pyqt4', 'pysqlite3', 'svn']
      )
