#!/usr/bin/env python
# $Id$
# Last modified Mon Feb 23 14:58:49 2009 on havoc
# update count: 73
# -*- coding:  utf-8 -*-

from pysqlite2 import dbapi2 as sqlite

"""
create database. Foŕ now a simple sqlite2 database is used
"""

def creatdb(dbpath):
    # Create a connection to the database file
    con = sqlite.connect(dbpath)
    
    # Get a Cursor object that operates in the context of Connection con:
    cur = con.cursor()

    # Create schema and test data
    #cur.execute("create table filelist(fileid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, filename TEXT)")
    #cur.execute("create table revlist(revnum INTEGER PRIMARY KEY, id INTEGER, FOREIGN KEY(id) REFERENCES filelist(fileid), logtext TEXT)")

    # Create the simpliest table 
    cur.execute("create table revlist(revnum INTEGER PRIMARY KEY,filename, logtext TEXT)")

    #cur.execute("insert into filelist(filename) values ('file1.cpp')")  
    #cur.execute("insert into filelist(filename) values ('file3.cpp')")
    #cur.execute("insert into filelist(filename) values ('file8.cpp')")

    cur.execute("insert into revlist(revnum,filename,author,logtext) values (1,'file8.cpp','initial commit')")


#cur.execute("select * from filelist")
    cur.execute("select * from revlist")

print cur.fetchall()

