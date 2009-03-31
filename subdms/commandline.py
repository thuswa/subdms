#!/usr/bin/env python
# $Id$
# Last modified Wed Apr  1 00:33:59 2009 on violator
# update count: 327
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

import os

import database
import frontend

"""
Command line interface class. 
"""

class cli:
    def __init__(self):
        """ Initialize database """
        self.db = database.sqlitedb()
        self.doc = frontend.document()
        
    def parseargs(self, args):
        """ Parse the args list and start actions accordingly."""
        shorthelp = "Type 'subdms help' for usage."

        # Display help 
        if args[1] == "help" or args[1] == "--help" or args[1] == "-h":
            self.dislayhelp()
            return

        # Check for valid number of arguments
        if len(args) > 6:
            raise Error, "To manny arguments. "+shorthelp  
        
        if len(args) < 5:
            raise Error, "To few arguments. "+shorthelp  

        # Check if "add" is given as argument 
        if args[1] == "add":
            # Get filename and check if file exists
            addfilepath = os.path.abspath(args[2])
            if not os.path.exists(addfilepath):
                raise FileError, "Filename "+filnamepath+" does not exist."

            # Get project and check if it exists
            project = args[3]
            if not self.db.projexists(project):
                raise DMSError, "Project "+project+" does not exist."

            # Get doctype and check if it exists
            doctype = args[4]
            if not doctype in self.db.getdoctypes(project):
                raise DMSError, "Doctype "+doctype+" does not exist for "\
                      "project "+project

            # Check if title is given as argument 
            if len(args) == 6:
                title = args[5]
            else:
                title = os.path.split(filename)[-1].rsplit(".")[0]

            # Finally call adddocument     
            self.adddocument(filename, project, doctype, title)
        else:
            print shorthelp
            
    def displayhelp(self):
        """ Display help text. """
        print "Usage: subdms add filename project doctype [title]"
        print
        print "This command line inteface makes it possible to add documents"
        print "in the DMS"
        print "If no title is given the filename without extension is"
        print "is set as title"
        
    def adddocument(self, addfilepath, project, doctype, doctitle):
        """ Add document fom command line. """

        issue = '1'
        filetype = addfilepath.rsplit('.')[-1]
        docnamelist = self.doc.createdocnamelist(project, doctype, issue, \
                                                 filetype)
        self.doc.adddocument(addfilepath, docnamelist, doctitle)
            
