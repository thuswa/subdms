#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 00:57:31 2009 on violator
# update count: 75

from distutils.core import setup


#args = sys.argv[:]
#
#for arg in args:
#	print arg
#	if string.find(arg, '--with-wsfc=') == 0:
#		WSFC_HOME = string.split(arg, '=')[1]
#		sys.argv.remove(arg)
#	elif string.find(arg, 'install') == 0:
#		INSTALL_OP = True
#

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
#      package_data = {'' : '' },
      scripts = ['subdms/subdms', 'subdms/subdms-server'],
      platforms='any',
      requires=['pysvn', 'pyqt4', 'pysqlite3', 'svn']
      )
