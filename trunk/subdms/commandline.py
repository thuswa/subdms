#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  7 19:07:47 2010 on stalker
# update count: 291
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
import sys

from . import database
from . import lowlevel
from . import frontend

from subdms import __version__

"""
Command-line interface class. 
"""

class cli:
    def __init__(self):
        """ Initialize dependency classes """
        self.conf = lowlevel.config()
        self.db = database.sqlitedb()
        self.doc = frontend.document()
        self.proj = frontend.project()
        self.state = frontend.docstate()
        self.link = lowlevel.linkname()
        self.category = self.conf.categories[0]

        self.shorthelp = "Type 'subdms help' for usage."

    def parseargs(self, args):
        """ Parse the args list and start actions accordingly."""

        # Display help 
        if args[1] == "help" or args[1] == "--help" or args[1] == "-h":
            self.displayhelp(args)
            return

        if args[1] == "add":
            self.addaction(args)
        elif args[1] == "create":
            self.createaction(args)
        elif args[1] == "list":
            # Check no of arguments
            self.checknoarg(args, 3, 3)
            if args[2] == "documents":
                self.listdocaction()
            elif args[2] == "projects":
                self.listprojaction()
            elif args[2] == "templates":
                self.listtmplaction()
        else:
            print(self.shorthelp)
            
    def displayhelp(self, args):
        """ Display help text. """
        if len(args) < 3:
            self.disptophelp()
        elif args[2] == "add":
            print("add: Add document files to the DMS.")
            print("Usage: subdms add filename project doctype [title]")
            print()
            print("Example:")
            print(" > subdms add filename.txt myproject note \"Technical note\"")
            print("or:")
            print(" > subdms add \"this project note.txt\" myproject note")
            print()
            print("This command-line interface makes it possible to add " \
                  "documents in the DMS.")
            print("It is a complement to add files via the graphical "\
                  "user interface,")
            print("which opens for the possibility to write scripts to " \
                  "automate this process.")              
            print("If you enter a title, make sure the title is a single " \
                  "string i.e. put it within \"\"")
            print("If no title is given the file name without extension is "\
                  "set as title.")
            print()
        elif args[2] == "create":
            print("create: Create a new project.")
            print("Usage: subdms create acronym projectname doctypes")
            print()
            print("Example:")
            print(" > subdms create LTE \"Long Term Evolution\" " \
                  "\"NOTE REPORT LIST SPEC\"")
            print()
            print("Note the \"\" around both the project name and the list " \
                  "of document types.") 
            print()
        elif args[2] == "list":
            print("list: List documents, projects or templates.")
            print("Usage:")
            print("       1. subdms list documents")
            print("       2. subdms list projects")
            print("       3. subdms list templates")
            print()
        else:
            self.disptophelp()
            
    def disptophelp(self):
        """ Display help about available subcommands."""
        print("usage: subdms <subcommand> [options]")
        print("Subdms command-line client, version "+__version__)
        print("Type 'svn help <subcommand>' for help on a specific " \
              "subcommand.")
        print()
        print("Available subcommands:")
        print("   add")
        print("   create")
        print("   list")

        
    def addaction(self, args):
        """ Add document from command line. """
        # Check no of arguments
        self.checknoarg(args, 5, 6)

        # Get file name and check if file exists
        addfilepath = os.path.abspath(args[2])
        if not os.path.exists(addfilepath):
            sys.exit("File "+addfilepath+" does not exist.")
            
        # Get file extension and check if it is supported 
        filetype = addfilepath.rsplit('.')[-1]
        if not filetype in self.conf.getsupportedfiletypes():
            sys.exit("Error: File extension ."+filetype+" is not " \
                     "supported. \n See documentation on supported " \
                     "file types.")
            
        # Get project and check if it exists
        project = args[3].upper()
        if not self.db.projexists(self.category, project):
            sys.exit("Error: Project "+project+" does not exist.")

        # Get doctype and check if it exists
        doctype = args[4].upper()
        if not doctype in self.db.getdoctypes(self.category, project):
            sys.exit("Error: Doctype "+doctype+" does not exist for "\
                     "project "+project)

        # Check if title is given as argument 
        if len(args) == 6:
            doctitle = args[5]
        else:
            doctitle = os.path.split(addfilepath)[-1].rsplit(".")[0]

        # Finally call adddocument     
        issue = '1'
        dockeywords=""
        docnamelist = self.link.const_docnamelist(self.category, project, \
                                                  doctype, issue, \
                                                 filetype)
        self.doc.adddocument(addfilepath, docnamelist, doctitle, dockeywords)

    def createaction(self, args):
        """ Create project from command-line. """
        # Check no of arguments
        self.checknoarg(args, 4, 5)

        acronym = args[2].upper()
        name = args[3]

        # Check if doctypes is given as argument 
        if len(args) == 5:
            doctypes = args[4].upper().rsplit(" ")
        else:
            doctypes = self.conf.doctypes.upper().rsplit(",")
        
        if not acronym:
            sys.exit("Error: Project acronym must be given as input.")
        elif self.db.projexists(self.category, acronym):
            sys.exit("Error: Project "+acronym+" already exists " \
                     "in category "+self.category)
        else:
            print(acronym)
            print(name)
            print(doctypes)
            self.proj.createproject(self.category, acronym, name, doctypes)

    def listdocaction(self):
        """ List the existing documents. """
        self.doclistheader()
        self.listdocuments(self.db.getalldocs())

    def listprojaction(self):
        """ List the existing projects. """
        self.projlistheader()
        for proj in self.db.getallprojs():
            print("%7s, %22s, %12s, %20s, %s" \
                  % (proj[2], proj[3], proj[4], proj[5][0:19], proj[6]))

    def listtmplaction(self):
        """ List the existing templates. """
        self.doclistheader()
        self.listdocuments(self.db.getalltmpls())        

    def listdocuments(self, docs):
        """ List the existing documents. """
        for doc in docs:
            docnamelist = list(doc[1:7])
            state = self.state.getstate(docnamelist)[0]
            docid = self.link.const_docid(docnamelist)
            title = doc[7].replace("\n" , " || ")
            doctype = doc[6]
            issue = doc[5]
            status = doc[8]
            print("%2s, %23s, %37s, %5s, %6s, %9s" % (state, docid, title, \
                  doctype, issue, status))

    def checknoarg(self, args, minarg, maxarg):
        """Check for valid number of arguments.  """
        if len(args) > maxarg:
            sys.exit("To many arguments. "+self.shorthelp)  
        
        if len(args) < minarg:
            sys.exit("To few arguments. "+self.shorthelp)  

    def doclistheader(self):
        """ Header for document list print out. """
        print(" S       Document Id                    Document Title       " \
              "       Type   Issue     Status   ")
        print("-- ------------------------ ---------------------------------" \
              "----- ------ ------- ------------")

    def projlistheader(self):
        """ Header for project list print out. """
        print("Acronym        Description        Created by       " \
              "Date Created           Document types")
        print("-------  ----------------------  ------------  " \
              "--------------------  ------------------------")

