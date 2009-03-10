#!/usr/bin/env python
# $Id$
# Last modified Tue Mar 10 21:58:59 2009 on violator
# update count: 113
# -*- coding:  utf-8 -*-

from pysqlite2 import dbapi2 as sqlite

"""
Database class. For now a simple sqlite2 database is used.
"""

class sqlitedb:
    def __init__(self, dbpath):
        """ Initialize database """
        # Create a connection to the database file
        con = sqlite.connect(dbpath)
        # Get a Cursor object that operates in the context of Connection con:
        self.cursor= con.cursor()
        
    def createdb(self):
        """ Create database """
        # Create the simpliest table 
        self.cursor.execute("create table revlist(revnum INTEGER PRIMARY KEY," \
                            "project, doctype, docno, docext, doctitle," \
                            "date, status, author, logtext TEXT)")
    def dumpdb(self):
        """ dump the whole database to standard output. """
        self.cursor.execute("select * from revlist")
        print self.cursor.fetchall()

