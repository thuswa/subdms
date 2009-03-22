#!/usr/bin/env python
# $Id$
# Last modified Sun Mar 22 22:33:56 2009 on violator
# update count: 458
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

from aboutui import Ui_AboutDialog
from createdocumentui import Ui_New_Document_Dialog
from createprojui import Ui_New_Project_Dialog
from mainwindow import Ui_MainWindow

docs = lowlevel.docname()
db = database.sqlitedb()

class ClientUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.aboutdialog = aboutDialog()
        self.projdialog = projectDialog()
        self.docdialog = documentDialog()
        
        # Set column width on list object
        self.ui.documentlist.setColumnWidth(0, 40)
        self.ui.documentlist.setColumnWidth(1, 140)
        self.ui.documentlist.setColumnWidth(2, 380)
        self.ui.documentlist.setColumnWidth(3, 100)

        # Connect menubar entries
        # Create menu
        self.connect(self.ui.actionNew_Project, QtCore.SIGNAL("activated()"), \
                     self.projdialog.show)
        self.connect(self.ui.actionNew_Document, QtCore.SIGNAL("activated()"), \
                     self.showdocdialog)
        self.connect(self.ui.actionNew_Issue, QtCore.SIGNAL("activated()"), \
                     self.newissue)        
        # Tools menu
        self.connect(self.ui.actionEdit_Document, \
                     QtCore.SIGNAL("activated()"), self.editdoc)
        self.connect(self.ui.actionCheck_in_Document, \
                     QtCore.SIGNAL("activated()"), self.checkindoc)
        self.connect(self.ui.actionCommit_Changes, \
                     QtCore.SIGNAL("activated()"), self.commitdoc)        
        self.connect(self.ui.actionRelease_Document, \
                     QtCore.SIGNAL("activated()"), self.releasedoc)
        self.connect(self.ui.actionList_Documents, \
                     QtCore.SIGNAL("activated()"), self.setdocumentlist)
        # Help menu
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), \
                     self.showaboutdialog)

    def showaboutdialog(self):
        """ Show about dialog """
        self.aboutdialog.show()
        
    def showdocdialog(self):
        """ Show create document dialog """
        self.docdialog.setprojlist()
        self.docdialog.setdoctypelist(self.docdialog.selectedproject())
        self.docdialog.show()
    
    def setdocumentlist(self):
        """ List the existing documents """
        n = 0
        for doc in db.getalldocs():
            docnamelist = list(doc[1:5])
            state = QtGui.QTableWidgetItem(self.doc.getstate(docnamelist))
            docname = QtGui.QTableWidgetItem(docs.const_docname(docnamelist))
            title = QtGui.QTableWidgetItem(doc[5])
            status = QtGui.QTableWidgetItem(doc[7])
            self.ui.documentlist.setItem(n, 0, state)
            self.ui.documentlist.setItem(n, 1, docname)
            self.ui.documentlist.setItem(n, 2, title)
            self.ui.documentlist.setItem(n, 3, status)
            n += 1        

    def getselecteddoc(self):
        """ Get the document selected in list """
        row = self.ui.documentlist.currentRow()
        docitem = self.ui.documentlist.item(row, 1)
        if docitem:
            return docs.deconst_docfname(unicode(docitem.text())+'.txt') #fixme
        else:
            return None

    def checkindoc(self):
        """ Check-in document action """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            message = self.doc.checkin(docnamelist)
            self.ui.statusbar.showMessage(message, 1000)

    def editdoc(self):
        """ Edit document action. """
        docnamelist = self.getselecteddoc()
        self.ui.statusbar.showMessage("Launching editor", 1000)
        self.doc.editdocument(docnamelist)

    def commitdoc(self):     
        """ Commit changes on document """
        docnamelist = self.getselecteddoc()
        text, ok = QtGui.QInputDialog.getText(self, \
                            'Commit changes', 'Enter commit message:')
        if ok:
            self.doc.commit(docnamelist, unicode(text))
            
    def releasedoc(self):     
        """ Release the document action. """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            message = self.doc.release(docnamelist)
            self.ui.statusbar.showMessage(message, 1000)

    def newissue(self):     
        """ Create a new issue """
        return None

class aboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        
class projectDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.proj = frontend.project()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Project_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.New_Project_Confirm, QtCore.SIGNAL("accepted()"), \
                     self.okaction)

    def okaction(self):
        proj = unicode(self.ui.Project_name.text())
        if db.projexists(proj):
            QtGui.QMessageBox.critical(None, "Error", \
                                       "Project "+proj+" already exists")
        else:
            self.proj.createproject(proj)
            self.close()

class documentDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.doc = frontend.document()
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
        docnamelist = self.doc.createdocnamelist(project, doctype, docext)
        self.doc.createdocument(docnamelist, doctitle)
        self.close()

