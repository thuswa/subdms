#!/usr/bin/env python
# $Id$
# Last modified Sat Mar 14 22:17:14 2009 on violator
# update count: 294
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

from PyQt4 import QtGui
from PyQt4 import QtCore

import database
import frontend
import lowlevel

from createdocumentui import Ui_New_Document_Dialog
from createprojui import Ui_New_Project_Dialog
from mainwindow import Ui_MainWindow

docs = lowlevel.docname()
db = database.sqlitedb()

class ClientUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.projdialog = projectDialog()
        self.docdialog = documentDialog()
        
        # Set column width on list object
        self.ui.documentlist.setColumnWidth(0, 140)
        self.ui.documentlist.setColumnWidth(1, 380)
        self.ui.documentlist.setColumnWidth(2, 100)

        # Connect buttons 
        self.connect(self.ui.new_project_button, QtCore.SIGNAL('clicked()'), \
                     self.projdialog.show)
        self.connect(self.ui.new_document_button, QtCore.SIGNAL('clicked()'), \
                     self.showdocdialog)
        self.connect(self.ui.list_documents_button, \
                     QtCore.SIGNAL('clicked()'), self.setdocumentlist)
        self.connect(self.ui.edit_document_button, \
                     QtCore.SIGNAL('clicked()'), self.setdocumentlist)
        self.connect(self.ui.checkin_document_button, \
                     QtCore.SIGNAL('clicked()'), self.setdocumentlist)     

    def showdocdialog(self):
        self.docdialog.setprojlist()
        self.docdialog.setdoctypelist(self.docdialog.selectedproject())
        self.docdialog.show()
    
    def setdocumentlist(self):
        n = 0
        for doc in db.getalldocs():
            docname = QtGui.QTableWidgetItem(docs.const_docname(list(doc[1:5])))
            title = QtGui.QTableWidgetItem(doc[5])
            status = QtGui.QTableWidgetItem(doc[7])
            self.ui.documentlist.setItem(n, 0, docname)
            self.ui.documentlist.setItem(n, 1, title)
            self.ui.documentlist.setItem(n, 2, status)
            n += 1        

class projectDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Project_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.New_Project_Confirm, QtCore.SIGNAL("accepted()"), \
                     self.okaction)

    def okaction(self):
        frontend.createproject(unicode(self.ui.Project_name.text()))
        self.close()

class documentDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Document_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.Select_Project_Box, \
                     QtCore.SIGNAL("activated(project)"),
                     self.setdoctypelist)

        self.connect(self.ui.New_Document_Confirm, \
                     QtCore.SIGNAL("accepted()"), self.okaction)

    def selectedproject(self):
        return unicode(self.ui.Select_Project_Box.currentText())

    def selecteddoctype(self):
        return unicode(self.ui.Select_Type_Box.currentText())
    
    def setprojlist(self):
        self.ui.Select_Project_Box.clear()
        for proj in db.getprojs():
            self.ui.Select_Project_Box.addItem(proj[0])

    def setdoctypelist(self, project):
        self.ui.Select_Type_Box.clear()
        for doctype in db.getdoctypes(project):
            self.ui.Select_Type_Box.addItem(doctype)
        
    def okaction(self):
        doctitle = unicode(self.ui.document_title.text())
        project = self.selectedproject()
        doctype = self.selecteddoctype()
        docext = "txt"
        docnamelist = frontend.createdocnamelist(project, doctype, docext)
        frontend.createdocument(docnamelist, doctitle)
        self.close()

