#!/usr/bin/env python
# $Id$
# Last modified Sat Sep  6 22:57:39 2008 on violator
# update count: 65

# create database
from pysqlite2 import dbapi2 as sqlite

# Create a connection to the database file
con = sqlite.connect("repodb")

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

