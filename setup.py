#!/usr/bin/env python
# $Id$
# Last modified Fri Mar 13 20:08:41 2009 on violator
# update count: 46

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
      package_dir = {'subdms' : 'subdms/lib' },
      platforms='any',
      requires=['pysvn', 'pyqt4', 'pysqlite3', 'svn']
      )
