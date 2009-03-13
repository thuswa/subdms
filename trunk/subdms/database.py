#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 00:37:09 2009 on violator
# update count: 170
# -*- coding:  utf-8 -*-

from pysqlite2 import dbapi2 as sqlite

import lowlevel

conf = lowlevel.dmsconfig()

"""
Database class. For now a simple sqlite2 database is used.
"""

class sqlitedb:
    def __init__(self):
        """ Initialize database """
        # Create a connection to the database file
        con = sqlite.connect(conf.dbpath)
        # Get a Cursor object that operates in the context of Connection con:
        self.cursor= con.cursor()
        
    def createdb(self):
        """ Create database """
        # Create the simpliest table 
        self.cursor.execute("create table revlist(revnum INTEGER PRIMARY KEY," \
                            "project, doctype, docno, docext, doctitle," \
                            "date, status, author, logtext TEXT)")

        self.cursor.execute("create table projlist(projname TEXT PRIMARY KEY," \
                            "doctypes)")

    def getalldocs(self):
        """ Get complete documents table from database. """
        self.cursor.execute("select * from revlist")
        return self.cursor.fetchall()

    def getallprojs(self):
        """ Get complete projects table from database. """
        self.cursor.execute("select * from projlist")
        return self.cursor.fetchall()

    def getprojs(self):
        """ Get list of all projects from database. """
        self.cursor.execute("select projname from projlist")
        return self.cursor.fetchall()

    def getdoctypes(self, project):
        """ Get doctypes list from a project from database. """
        self.cursor.execute("select doctypes from projlist " \
                            "where projname=?", (project, ))
        return self.cursor.fetchone()[0].split(",")

    def getdocno(self, project, doctype):
        """ Get document number from this project and type. """
        # Query database 
        self.cursor.execute("select max(docno) from revlist " \
                            "where project=? and doctype=?" \
                            , (project, doctype))
        # Get document number
        docno = self.cursor.fetchone()[0]

        # Check if docname is not None -> return zero 
        if not docno:
            docno = '0'
        return int(docno)

