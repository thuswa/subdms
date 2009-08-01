#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Sat Aug  1 16:01:50 2009 on violator
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
from PyQt4 import QtCore, QtGui

class iconDict(dict):
    """Stores icons by name, loads on demand"""
    iconExt = ['.png', '.bmp']
    def __init__(self):
        dict.__init__(self, {})
        self.pathList = []

    def addIconPath(self, potentialPaths):
        """Add first good path from potentialPaths"""
        for path in potentialPaths:
            try:
                for name in os.listdir(path):
                    pixmap = QtGui.QPixmap(os.path.join(path, name))
                    if not pixmap.isNull():
                        self.pathList.append(path)
                        return
            except OSError:
                pass

    def __getitem__(self, name):
        """Return icon, loading if necessary"""
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            icon = self.loadIcon(name)
            if not icon:
                raise
            return icon

    def loadAllIcons(self):
        """Load all icons available in self.pathList"""
        self.clear()
        for path in self.pathList:
            try:
                for name in os.listdir(path):
                    pixmap = QtGui.QPixmap(os.path.join(path, name))
                    if not pixmap.isNull():
                        name = os.path.splitext(name)[0]
                        try:
                            icon = self[name]
                        except KeyError:
                            icon = QtGui.QIcon()
                            self[name] = icon
                        icon.addPixmap(pixmap)
            except OSError:
                pass

    def loadIcon(self, iconName):
        """Load icon from iconPath, add to dictionary and return the icon"""
        icon = QtGui.QIcon()
        for path in self.pathList:
            for ext in IconDict.iconExt:
                fileName = iconName + ext
                pixmap = QtGui.QPixmap(os.path.join(path, fileName))
                if not pixmap.isNull():
                    icon.addPixmap(pixmap)
                if not icon.isNull():
                    self[iconName] = icon
                    return icon
        return None
