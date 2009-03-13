#!/usr/bin/env python
# $Id$
# Last modified Fri Mar 13 23:41:10 2009 on violator
# update count: 69

from distutils.core import setup

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
      description='A document management system (DMS) based on subversion',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      classifiers= CLASSIFIERS,
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
