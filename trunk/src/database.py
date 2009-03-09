#!/usr/bin/env python
# $Id$
# Last modified Mon Mar  9 23:59:08 2009 on violator
# update count: 103
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

    #cur.execute("insert into filelist(filename) values ('file1.cpp')")  
    #cur.execute("insert into filelist(filename) values ('file3.cpp')")
    #cur.execute("insert into filelist(filename) values ('file8.cpp')")

#    cur.execute("insert into revlist(revnum,filename,author,logtext) "\
#                "values (1,'file8.cpp','thuswa','initial commit')")

    #cur.execute("select * from filelist")
#    cur.execute("select * from revlist")

#    print cur.fetchall()

