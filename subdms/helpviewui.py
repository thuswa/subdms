#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Sat Aug  1 21:33:51 2009 on violator
# update count: 1173
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

import os.path
import sys
import webbrowser
from PyQt4 import QtCore, QtGui

class helpView(QtGui.QMainWindow):
    """Window for viewing an html help file"""

    def __init__(self, path, caption, icons, parent=None):
        """Helpview initialize with text"""
        QtGui.QMainWindow.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setStatusBar(QtGui.QStatusBar())
        self.textView = HelpViewer(self)
        self.setCentralWidget(self.textView)
        path = os.path.abspath(path)
        if sys.platform.startswith('win'):
            path = path.replace('\\', '/')
        self.textView.setSearchPaths([os.path.dirname(path)])
        self.textView.setSource(QtCore.QUrl('file:///%s' % path))
        self.resize(520, 440)
        self.setWindowTitle(caption)
        tools = self.addToolBar('Tools')
        self.menu = QtGui.QMenu(self.textView)
        self.connect(self.textView,
                     QtCore.SIGNAL('highlighted(const QString&)'),
                     self.showLink)

        backAct = QtGui.QAction('&Back', self)
        try:
            backAct.setIcon(icons['go-previous'])
        except KeyError:
            pass
        tools.addAction(backAct)
        self.menu.addAction(backAct)
        self.connect(backAct, QtCore.SIGNAL('triggered()'),
                     self.textView, QtCore.SLOT('backward()'))
        backAct.setEnabled(False)
        self.connect(self.textView, QtCore.SIGNAL('backwardAvailable(bool)'),
                     backAct, QtCore.SLOT('setEnabled(bool)'))

        forwardAct = QtGui.QAction('&Forward', self)
        try:
            forwardAct.setIcon(icons['go-next'])
        except KeyError:
            pass
        tools.addAction(forwardAct)
        self.menu.addAction(forwardAct)
        self.connect(forwardAct, QtCore.SIGNAL('triggered()'),
                     self.textView, QtCore.SLOT('forward()'))
        forwardAct.setEnabled(False)
        self.connect(self.textView, QtCore.SIGNAL('forwardAvailable(bool)'),
                     forwardAct, QtCore.SLOT('setEnabled(bool)'))

        homeAct = QtGui.QAction('&Home', self)
        try:
            homeAct.setIcon(icons['go-home'])
        except KeyError:
            pass
        tools.addAction(homeAct)
        self.menu.addAction(homeAct)
        self.connect(homeAct, QtCore.SIGNAL('triggered()'),
                     self.textView, QtCore.SLOT('home()'))

    def showLink(self, text):
        """Send link text to the statusbar"""
        self.statusBar().showMessage(unicode(text))


class HelpViewer(QtGui.QTextBrowser):
    """Shows an html help file"""
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)

    def setSource(self, url):
        """Called when user clicks on a URL"""
        name = unicode(url.toString())
        if name.startswith(u'http'):
            webbrowser.open(name, True)
        else:
            QtGui.QTextBrowser.setSource(self, QtCore.QUrl(name))

    def contextMenuEvent(self, event):
        """Popup menu on right click"""
        self.parentWidget().menu.exec_(event.globalPos())
