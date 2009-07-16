#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Thu Jul 16 13:25:10 2009 on violator
# update count: 92
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

import database
import lowlevel
import frontend

"""
Command-line interface class. 
"""

class cli:
    def __init__(self):
        """ Initialize dependency classes """
        self.conf = lowlevel.config()
        self.db = database.sqlitedb()
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        self.category = self.conf.categories[0]
        
    def parseargs(self, args):
        """ Parse the args list and start actions accordingly."""
        shorthelp = "Type 'subdms help' for usage."

        # Display help 
        if args[1] == "help" or args[1] == "--help" or args[1] == "-h":
            self.displayhelp()
            return

        # Check for valid number of arguments
        if len(args) > 6:
            sys.exit("To many arguments. "+shorthelp)  
        
        if len(args) < 5:
            sys.exit("To few arguments. "+shorthelp)  

        # Check if "add" is given as argument 
        if args[1] == "add":
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
                title = args[5]
            else:
                title = os.path.split(addfilepath)[-1].rsplit(".")[0]

            # Finally call adddocument     
            self.adddocument(addfilepath, filetype, project, doctype, title)

        # Check if "create" is given as argument 
#        elif args[1] == "create":
#            acronym = args[1].upper()
#            name = args[2]
#            doctypes = args[3].upper().replace(" ","").rsplit(",")
#
#            if not acronym:
#                sys.exit("Error: Project acronym must be given as input.")
#            elif db.projexists(self.category, acronym):
#                sys.exit("Error: Project "+acronym+" already exists " \
#                         "in category "+self.category)
#            else:
#                self.proj.createproject(category, acronym, name, doctypes)
        else:
            print shorthelp
            
    def displayhelp(self):
        """ Display help text. """
        print "Usage: subdms add filename project doctype [title]"
        print
        print "Example:"
        print " > subdms add filename.txt myproject note \"Technical note\""
        print "or:"
        print " > subdms add \"this project note.txt\" myproject note"
        print
        print "This command line interface makes it possible to add documents "\
              "in the DMS."
        print "It is a compliment to add files via the graphical "\
              "user interface."
        print "And opens for the possibility to write scripts to automate"\
              "the adding of files"              
        print "If you enter a title, make sure the title is a string"
        print "If no title is given the file name without extension is "\
              "set as title."
        
    def adddocument(self, addfilepath, filetype, project, doctype, doctitle):
        """ Add document from command line. """
        
        issue = '1'
        dockeywords=""
        docnamelist = self.link.const_docnamelist(self.category, project, \
                                                  doctype, issue, \
                                                 filetype)
        self.doc.adddocument(addfilepath, docnamelist, doctitle, dockeywords)
            
