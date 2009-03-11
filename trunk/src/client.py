#!/usr/bin/env python
# $Id$
# Last modified Thu Mar 12 00:53:41 2009 on violator
# update count: 210

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
        
        # Set column width on list object
        self.ui.documentlist.setColumnWidth(0, 120)
        self.ui.documentlist.setColumnWidth(1, 400)
        self.ui.documentlist.setColumnWidth(2, 100)
        self.connect(self.ui.new_project_button, QtCore.SIGNAL('clicked()'), \
                     self.projdialog.show)
        self.connect(self.ui.list_documents_button, \
                     QtCore.SIGNAL('clicked()'), self.setdocumentlist)

    def setdocumentlist(self):
        n = 0
        for doc in db.getall():
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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clientapp = ClientUi()
    clientapp.show()
    sys.exit(app.exec_())
