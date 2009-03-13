#!/usr/bin/env python
# $Id$
# Last modified Thu Mar 12 23:51:06 2009 on violator
# update count: 287
# -*- coding:  utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import database
import frontend
import lowlib

from createdocumentui import Ui_New_Document_Dialog
from createprojui import Ui_New_Project_Dialog
from mainwindow import Ui_MainWindow

docs = lowlib.docname()
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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clientapp = ClientUi()
    clientapp.show()
    sys.exit(app.exec_())
