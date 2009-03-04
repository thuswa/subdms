#!/usr/bin/env python
# $Id$
# Last modified Wed Mar  4 22:22:24 2009 on violator
# update count: 37

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import createdocumentui
import createprojui
import frontend
import mainwindow

# Ui_MainWindow

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


app = QtGui.QApplication(sys.argv)
icon = InputDialog()
icon.show()
app.exec_()

#sys.exit(app.exec_())
