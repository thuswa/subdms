#!/usr/bin/env python
# $Id$
# Last modified Mon Apr 13 21:49:25 2009 on violator
# update count: 302
# -*- coding:  utf-8 -*-
#
# subdms - A document management system based on subversion.
# Copyright (C) 2009  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pysqlite2 import dbapi2 as sqlite
import string

import lowlevel

"""
Database class. For now a simple sqlite2 database is used.
"""

class sqlitedb:
    def __init__(self):
        """ Initialize database """
        self.conf = lowlevel.config()
        # Create a connection to the database file
        self.con = sqlite.connect(self.conf.dbpath)
        # Get a Cursor object that operates in the context of Connection con:
        self.cursor= self.con.cursor()
        
    def createdb(self):
        """ Create database """
        # Create the simpliest table 
        self.cursor.execute("create table revlist(revnum INTEGER PRIMARY KEY," \
                            "category, project, doctype, docno, issue, " \
                            "docext, doctitle, date, status, author, " \
                            "logtext TEXT)")

        self.cursor.execute("create table projlist(projname TEXT PRIMARY KEY," \
                            "doctypes)")

        print "Create database: "+self.conf.dbpath

    def writerevlist(self,rvn, writestr):
        """ Write to documents table in database. """
        # Construct sql command string
        db_str="insert into revlist(revnum, category, project, doctype, " \
                "docno, issue, docext, doctitle, date, status, author, " \
                "logtext) values(\"%s\", \"%s\")" \
                % (rvn, string.join(writestr, "\",\""))
        # Excecute sql command
        self.cursor.execute(db_str)
        self.con.commit()

    def writeprojlist(self, projname, doctypes):
        """ Write to project table in database. """
        # Construct sql command string
        db_str="insert into projlist(projname, doctypes) " \
                "values(\"%s\", \"%s\")" \
                % (projname, string.join(doctypes,","))
        # Excecute sql command
        self.cursor.execute(db_str)
        self.con.commit()

    def statuschg(self, docnamelist, status):
        """ Update document status """
        d = docnamelist
        self.cursor.execute("update revlist set status=? " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?" , \
                            (status, d[0], d[1], d[2], d[3], d[4] ))
        self.con.commit()
        
    def getalldocs(self):
        """ Get complete documents table from database. """
        self.cursor.execute("select * from revlist " \
                            "where category = \"P\"")
        return self.cursor.fetchall()

    def getallprojs(self):
        """ Get complete projects table from database. """
        self.cursor.execute("select * from projlist " \
                            "where projname != \"TMPL\"")
        return self.cursor.fetchall()

    def getalltmpls(self):
        """ Get complete templates table from database. """
        self.cursor.execute("select * from revlist " \
                            "where category = \"T\"")
        return self.cursor.fetchall()

    def getprojs(self):
        """ Get list of all projects from database. """
        self.cursor.execute("select projname from projlist "
                            "where projname != \"TMPL\"")
        return self.cursor.fetchall()

    def projexists(self, project):
        """ Check if project exists in database. """
        self.cursor.execute("select * from projlist "
                            "where projname=?", (project, ))
        if self.cursor.fetchall():
            return True
        else:
            return False

    def docexists(self, documentid, issue):
        """ Check if project exists in database. """
        category, project, doctype, docno = documentid.split("-")
        # Query database 
        self.cursor.execute("select * from revlist " \
                            "where category=? project=? and doctype=? "\
                            "and docno=? and issue=?", \
                            (category, project, doctype, docno, issue, ))
        if self.cursor.fetchall():
            return True
        else:
            return False

    def getdoctypes(self, project):
        """ Get doctypes list from a project from database. """
        self.cursor.execute("select doctypes from projlist " \
                            "where projname=?", (project, ))
        return self.cursor.fetchone()[0].split(",")

    def getdocno(self, category, project, doctype):
        """ Get document number from this project and type. """
        # Query database 
        self.cursor.execute("select max(docno) from revlist " \
                            "where category = ? and project=? and doctype=?" \
                            , (category, project, doctype))
        # Get document number
        docno = self.cursor.fetchone()[0]

        # Check if docname is not None -> return zero 
        if not docno:
            docno = '0'
        return int(docno)

    def getdocext(self, documentid, issue):
        """ Get document file type. """
        # Query database
        category, project, doctype, docno = documentid.split("-")
        self.cursor.execute("select docext from revlist " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?", \
                            (category, project, doctype, docno, issue, ))
        return self.cursor.fetchone()[0]

    def gettemplates(self, filetype):
        """ Get templates of one file type from database. """
        self.cursor.execute("select * from revlist " \
                            "where category = \"T\" and docext=? and " \
                            "status=\"released\"", (filetype, ))
        return self.cursor.fetchall()

    def getdocumentinfo(self, docnamelist):
        """ Get all info about document. """
        d = docnamelist
        self.cursor.execute("select * from revlist " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?" , \
                            (d[0], d[1], d[2], d[3], d[4] ))
        return self.cursor.fetchall()[0]
