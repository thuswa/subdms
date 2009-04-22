#!/usr/bin/env python
# $Id$
# Last modified Thu Apr 23 00:10:02 2009 on violator
# update count: 583
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

import epoch
import lowlevel

"""
Database class. For now a simple sqlite2 database is used.
"""

class sqlitedb:
    def __init__(self):
        """ Initialize database """
        self.conf = lowlevel.config()
        self.dt = epoch.dtime()
        # Create a connection to the database file
        self.con = sqlite.connect(self.conf.dbpath)
        # Get a Cursor object that operates in the context of Connection con:
        self.cursor= self.con.cursor()
        
    def createdb(self):
        """ Create database """
        # Create the simpliest table 
        self.cursor.execute("create table doclist(revnum INTEGER PRIMARY KEY," \
                            "category, project, doctype, docno, issue, " \
                            "docext, doctitle, status, author, keywords, " \
                            "cdate, rdate, odate)")

        self.cursor.execute("create table revlist(revnum INTEGER PRIMARY KEY," \
                            "category, project, doctype, docno, issue, " \
                            "revdate, author, logtext TEXT)")

        self.cursor.execute("create table projlist(revnum INTEGER PRIMARY KEY,"\
                            "category, acronym, description, author, date, " \
                            "doctypes TEXT)")

        print "Create database: "+self.conf.dbpath

    def writedoclist(self, rvn, writestr):
        """ Write to documents table in database. """
        # Construct sql command string
        db_str="insert into doclist(revnum, category, project, doctype, " \
                "docno, issue, docext, doctitle, status, author, " \
                "keywords, cdate, rdate, odate) values(\"%s\", \"%s\")" \
                % (rvn, string.join(writestr, "\",\""))
        # Excecute sql command
        self.cursor.execute(db_str)
        self.con.commit()

    def writerevlist(self, rvn, writestr):
        """ Write to revision table in database. """
        # Construct sql command string
        db_str="insert into revlist(revnum, category, project, doctype, " \
                "docno, issue, revdate, author, logtext) " \
                "values(\"%s\", \"%s\")" \
                % (rvn, string.join(writestr, "\",\""))
        # Excecute sql command
        self.cursor.execute(db_str)
        self.con.commit()

    def writeprojlist(self, rvn, writestr):
        """ Write to project table in database. """
        # Construct sql command string
        db_str="insert into projlist(revnum, category, acronym, description, "\
                "author, date) values(\"%s\", \"%s\")" \
                % (rvn, string.join(writestr, "\",\""))
        # Excecute sql command
        self.cursor.execute(db_str)
        self.con.commit()

    def doctypechg(self, category, project, doctype):
        """ Update document type list. """
        doctypes = self.getdoctypes(category, project)
        if doctypes:
            doctypes = doctypes+","+doctype
        else:
            doctypes = doctype

        self.cursor.execute("update projlist set doctypes=? " \
                            "where category=? and acronym=?" , \
                            (doctypes, category, project ))
        self.con.commit()

    def updatedoclist(self, docnamelist, datastr, data):
        """ Generic doclist update method. """
        d = docnamelist
        self.cursor.execute("update doclist set "+datastr+"=? " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?" , \
                            (data, d[0], d[1], d[2], d[3], d[4] ))
        self.con.commit()
        
    def statuschg(self, docnamelist, status, date):
        """ Update document status. """
        if status == "released":
            self.updatedoclist(docnamelist, "rdate", date)
        if status == "obsolete":
            self.updatedoclist(docnamelist, "odate", date)

        self.updatedoclist(docnamelist, "status", status)    

    def titlechg(self, docnamelist, title):
        """ Update document title. """
        self.updatedoclist(docnamelist, "doctitle", title)    
        
    def keywordchg(self, docnamelist, keywords):
        """ Update document keywords """
        self.updatedoclist(docnamelist, "keywords", keywords)    

    def getalldocs(self):
        """ Get complete documents table from database. """
        self.cursor.execute("select * from doclist " \
                            "where category = \"P\"")
        return self.cursor.fetchall()

    def getallprojs(self):
        """ Get complete projects table from database. """
        self.cursor.execute("select * from projlist " \
                            "where acronym != \"TMPL\"")
        return self.cursor.fetchall()

    def getallrev(self):
        """ Get complete revision table from database. """
        self.cursor.execute("select * from revlist")
        return self.cursor.fetchall()

    def getalltmpls(self):
        """ Get complete templates table from database. """
        self.cursor.execute("select * from doclist " \
                            "where category = \"T\"")
        return self.cursor.fetchall()

    def dumpallprojs(self):
        """ Dump projects table from database. """
        self.cursor.execute("select * from projlist")
        return self.cursor.fetchall()

    def getprojs(self):
        """ Get list of all projects from database. """
        self.cursor.execute("select acronym from projlist " \
                            "where acronym != \"TMPL\"")
        return self.cursor.fetchall()

    def getprojdesc(self, category, project):
        """ Get projects description from database. """
        self.cursor.execute("select description from projlist " \
                            "where category=? and acronym=?" , \
                            (category, project ))
        return self.cursor.fetchone()[0]

    def projexists(self, category, project):
        """ Check if project exists in database. """
        self.cursor.execute("select * from projlist " \
                            "where category=? and acronym=?" , \
                            (category, project ))

        if self.cursor.fetchall():
            return True
        else:
            return False

    def docexists(self, documentid, issue):
        """ Check if project exists in database. """
        category, project, doctype, docno = documentid.split("-")
        # Query database 
        self.cursor.execute("select * from doclist " \
                            "where category=? project=? and doctype=? "\
                            "and docno=? and issue=?", \
                            (category, project, doctype, docno, issue, ))
        if self.cursor.fetchall():
            return True
        else:
            return False

    def getdoctypes(self, category, project):
        """ Get doctypes list from a project from database. """
        self.cursor.execute("select doctypes from projlist " \
                            "where category=? and acronym=?", \
                            (category, project,  ))
        return self.cursor.fetchone()[0]

    def getdocno(self, category, project, doctype):
        """ Get document number from this project and type. """
        # Query database 
        self.cursor.execute("select max(docno) from doclist " \
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
        self.cursor.execute("select docext from doclist " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?", \
                            (category, project, doctype, docno, issue, ))
        return self.cursor.fetchone()[0]

    def gettemplates(self, filetype):
        """ Get templates of one file type from database. """
        self.cursor.execute("select * from doclist " \
                            "where category = \"T\" and docext=? and " \
                            "status=\"released\"", (filetype, ))
        return self.cursor.fetchall()

    def getdocumentinfo(self, docnamelist):
        """ Get all info about document. """
        d = docnamelist
        self.cursor.execute("select * from doclist " \
                            "where category=? and project=? and doctype=? " \
                            "and docno=? and issue=?" , \
                            (d[0], d[1], d[2], d[3], d[4] ))
        return self.cursor.fetchall()[0]
    
    def upgradedoclist(self, doclist):
        """ Upgrade doclist table and revlist. """

        for doc in doclist: 
            [rvn, project, doctype, docno, issue, docext, doctitle, cdate, \
             status, author, log_message] = doc

            docnamelist = ["P", project.upper(), doctype.upper(), docno, \
                           issue, docext]      
            dockeywords = ""
            rdate = ""
            odate = ""

            if status == "released":
                rdate = self.dt.datetimestamp()
            if status == "obsolete":
                rdate = self.dt.datetimestamp()
                odate = rdate
                
            writestr=[]
            writestr.extend(docnamelist)
            writestr.extend([doctitle, status, author, dockeywords, cdate, \
                             rdate, odate])
            self.writedoclist(rvn, writestr)
            
            writestr = writestr[0:5]
            writestr.append(cdate)
            writestr.extend([author, log_message])
            # Write data to db
            self.writerevlist(rvn, writestr) 

    def upgradeprojlist(self, projlist):
        """ Upgrade projlist table. """
        rvn=1
        for proj in projlist:
            [projname, doctypes] = proj
            description = ""
            author = "upgrade"
            ddate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            writestr = ["P", projname, description, author, ddate, doctypes]
            db_str="insert into projlist(revnum, category, acronym, " \
                    "description, author, date, doctypes) " \
                    "values(\"%s\", \"%s\")" \
                    % (rvn, string.join(writestr, "\",\""))
            # Excecute sql command
            self.cursor.execute(db_str)
            self.con.commit()
            rvn += 1
