#!/usr/bin/env python
# $Id$
# Last modified Wed Mar 11 13:39:17 2009 on havoc
# update count: 133

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import frontend
from createdocumentui import Ui_New_Document_Dialog
from createprojui import Ui_New_Project_Dialog
from mainwindow import Ui_MainWindow

class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 350, 80)
        self.setWindowTitle('Subdms - Document Managment')
        self.setWindowIcon(QtGui.QIcon('kde.png'))


        self.button = QtGui.QPushButton('Create project', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), \
                     self.projectDialog)
        self.setFocus()

#        self.label = QtGui.QLineEdit(self)
#        self.label.move(160, 22)

    def projectDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, \
                'Subdms - Create project', 'Enter project name:')
        if ok:
            frontend.createproject(unicode(text))

class ClientUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set column width on list object
        self.ui.documentlist.setColumnWidth(0, 110)
        self.ui.documentlist.setColumnWidth(1, 400)
        self.ui.documentlist.setColumnWidth(2, 110)
        self.connect(self.ui.new_project_button, QtCore.SIGNAL('clicked()'), \
                     self.projectDialog)

    def projectDialog(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Project_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.connect(self.ui.New_Project_Confirm, QtCore.SIGNAL("accepted()"), QtCore.SLOT(frontend.createproject(unicode(self.ui.Project_name.displayText()))))
#        self.connect(self.ui.New_Project_Confirm.Cancel, QtCore.SIGNAL("rejected()"), QtCore.SLOT(self.ui.close()))
        def accept(self): 
            self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clientapp = ClientUi()
    clientapp.show()
    sys.exit(app.exec_())
