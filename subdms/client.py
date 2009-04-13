#!/usr/bin/env python
# $Id$
# Last modified Tue Apr 14 00:48:28 2009 on violator
# update count: 921
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
from documentinfoui import Ui_Document_Info_Dialog
from mainwindow import Ui_MainWindow

db = database.sqlitedb()

################################################################################

class ClientUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        self.status = frontend.docstatus()
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.aboutdialog = aboutDialog()
        self.projdialog = projectDialog()
        self.docdialog = documentDialog('P')
        self.tmpldialog = documentDialog('T')
        self.docinfodialog = documentInfoDialog()
        
        # Set column width on list object
        self.ui.documentlist.setColumnWidth(0, 40)
        self.ui.documentlist.setColumnWidth(1, 200)
        self.ui.documentlist.setColumnWidth(2, 420)
        self.ui.documentlist.setColumnWidth(3, 60)
        self.ui.documentlist.setColumnWidth(4, 60)
        self.ui.documentlist.setColumnWidth(5, 100)

        # Connect menubar entries
        # Create menu
        self.connect(self.ui.actionNew_Project, QtCore.SIGNAL("activated()"), \
                     self.projdialog.show)
        self.connect(self.ui.actionNew_Document, QtCore.SIGNAL("activated()"), \
                     self.showdocdialog)
        self.connect(self.ui.actionNew_Issue, QtCore.SIGNAL("activated()"), \
                     self.newissue)
        self.connect(self.ui.actionNew_Template, QtCore.SIGNAL("activated()"), \
                     self.showtmpldialog)
        # View menu
        self.connect(self.ui.actionList_Documents, \
                     QtCore.SIGNAL("activated()"), self.setdocumentlist)
        self.connect(self.ui.actionList_Templates, \
                     QtCore.SIGNAL("activated()"), self.settemplatelist)
        # Tools menu
        self.connect(self.ui.actionDocument_Info, \
                     QtCore.SIGNAL("activated()"), self.showdocinfo)
        self.connect(self.ui.actionEdit_Document, \
                     QtCore.SIGNAL("activated()"), self.editdoc)
        self.connect(self.ui.actionCheck_in_Document, \
                     QtCore.SIGNAL("activated()"), self.checkindoc)
        self.connect(self.ui.actionCommit_Changes, \
                     QtCore.SIGNAL("activated()"), self.commitdoc)        
        self.connect(self.ui.actionRelease_Document, \
                     QtCore.SIGNAL("activated()"), self.releasedoc)
        # Help menu
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), \
                     self.showaboutdialog)

        # Right-click menu = Tools
        self.connect(self.ui.documentlist, \
             QtCore.SIGNAL('customContextMenuRequested(const QPoint &)'), \
                     self.showrightclickmenu)

    def showdocinfo(self):
        docnamelist = self.getselecteddoc()
        self.docinfodialog.show()
        self.docinfodialog.setdocinfo(docnamelist)
        
    def showrightclickmenu(self, coord):
        coord = self.mapToGlobal(coord)
        self.ui.menuTools.popup(coord)
        
    def showaboutdialog(self):
        """ Show about dialog """
        self.aboutdialog.show()
 
    def showdocdialog(self):
        """ Show create document """        
        # Check if at least one project exist
        if not db.getallprojs():
            QtGui.QMessageBox.critical(None, "Error","No projects exist. "\
                                       "Use the \"New Project\" dialog to "\
                                       "create one.")
        else:
            self.docdialog.setprojlist()
            self.docdialog.setfiletypelist()
            self.docdialog.setdoctypelist(self.docdialog.selectedproject())
            self.docdialog.settmplnamelist(self.docdialog.selectedfiletype())
            self.docdialog.show()

    def showtmpldialog(self):
        """ Show create template """        
        self.tmpldialog.setprojlist()
        self.tmpldialog.setfiletypelist()
        self.tmpldialog.setdoctypelist(self.tmpldialog.selectedproject())
        self.tmpldialog.settmplnamelist(self.tmpldialog.selectedfiletype())
        self.tmpldialog.ui.Title_Label.setText("Template title:")
        self.tmpldialog.setWindowTitle("Create Template") 
        self.tmpldialog.show()

    def settemplatelist(self):
        """ List the existing templates """
        self.setlist(db.getalltmpls())        
    def setdocumentlist(self):
        """ List the existing documents """
        self.setlist(db.getalldocs())

    def setlist(self, docs):
        """ List the existing documents """
        self.ui.documentlist.clearContents()
        n = 0
        for doc in docs:
            docnamelist = list(doc[1:7])
            state = QtGui.QTableWidgetItem(self.doc.getstate(docnamelist)[0])
            docid = QtGui.QTableWidgetItem(self.link.const_docid(docnamelist))
            title = QtGui.QTableWidgetItem(doc[7])
            doctype = QtGui.QTableWidgetItem(doc[6])
            issue =  QtGui.QTableWidgetItem(doc[5])
            status = QtGui.QTableWidgetItem(doc[9])
            self.ui.documentlist.setItem(n, 0, state)
            self.ui.documentlist.setItem(n, 1, docid)
            self.ui.documentlist.setItem(n, 2, title)
            self.ui.documentlist.setItem(n, 3, doctype)
            self.ui.documentlist.setItem(n, 4, issue)
            self.ui.documentlist.setItem(n, 5, status)
            n += 1        

    def getselecteddoc(self):
        """ Get the document selected in list """
        row = self.ui.documentlist.currentRow()
        docitem = self.ui.documentlist.item(row, 1)
        typeitem = self.ui.documentlist.item(row, 3)
        issueitem = self.ui.documentlist.item(row, 4)
        if docitem:
            return self.link.deconst_docfname(unicode(docitem.text())+'-'+ \
                                              unicode(issueitem.text())+'.'+ \
                                              unicode(typeitem.text()))
        else:
            return None

    def checkindoc(self):
        """ Check-in document action """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            message = self.doc.checkin(docnamelist)
            self.ui.statusbar.showMessage(message, 1500)

    def editdoc(self):
        """ Edit document action. """
        docnamelist = self.getselecteddoc()
        self.ui.statusbar.showMessage("Launching editor", 1500)
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
            self.ui.statusbar.showMessage(message, 1500)

    def newissue(self):     
        """ Create a new issue. """
        docnamelist = self.getselecteddoc()
        if self.status.getstatus(docnamelist) != "released":
            QtGui.QMessageBox.critical(None, "Error",\
                                       "The selected document does not have "\
                                       "status \"released\". A new issue can "\
                                       "not be created unless the current "\
                                       "issue has first been released.")
        else:
            if docnamelist:
                message = self.doc.newissue(docnamelist)
                self.ui.statusbar.showMessage(message, 1500)

################################################################################
            
class aboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

################################################################################

class projectDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.proj = frontend.project()
        self.conf = lowlevel.config()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Project_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.New_Project_Confirm, QtCore.SIGNAL("accepted()"), \
                     self.okaction)

    def okaction(self):
        proj = unicode(self.ui.Project_name.text()).upper()
        if db.projexists(proj):
            QtGui.QMessageBox.critical(None, "Error", \
                                       "Project "+proj+" already exists")
        else:
            self.proj.createproject("P", proj, self.conf.doctypes)
            self.close()

################################################################################
            
class documentDialog(QtGui.QDialog):
    def __init__(self, category, parent=None):
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        self.conf = lowlevel.config()
        self.addfile = addFileDialog()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Document_Dialog()
        self.ui.setupUi(self)
        self.cat = category
        self.tmpllist = []
        
        # Connect comboboxes and buttons
        self.connect(self.ui.Select_Project_Box, \
                     QtCore.SIGNAL("activated(project)"),
                     self.setdoctypelist)
        self.connect(self.ui.File_Type_Box, \
                     QtCore.SIGNAL("activated(filetype)"),
                     self.settmplnamelist)

        self.connect(self.ui.Open_File_Dialog, \
                     QtCore.SIGNAL("pressed()"), self.addfileaction)

        self.connect(self.ui.New_Document_Confirm, \
                     QtCore.SIGNAL("accepted()"), self.okaction)

    # Selected combobox item functions   
    def selectedproject(self):
        return unicode(self.ui.Select_Project_Box.currentText())

    def selecteddoctype(self):
        return unicode(self.ui.Select_Type_Box.currentText())

    def selectedfiletype(self):
        return unicode(self.ui.File_Type_Box.currentText())

    def selectedtemplate(self):
        n = self.ui.Template_Name_Box.currentIndex()
        return self.tmpllist[n*6:n*6+6]

    # Set combobox functions
    def setprojlist(self):
        self.ui.Select_Project_Box.clear()
        if self.cat == "P":
            for proj in db.getprojs():
                self.ui.Select_Project_Box.addItem(proj[0])
        else:
            self.ui.Select_Project_Box.addItem("TMPL")
            
    def setdoctypelist(self, project):
        self.ui.Select_Type_Box.clear()
        for doctype in db.getdoctypes(project):
            self.ui.Select_Type_Box.addItem(doctype)

    def setfiletypelist(self):
        self.ui.File_Type_Box.clear()
        for filetype in self.conf.filetypes:
            if db.gettemplates(filetype):
                self.ui.File_Type_Box.addItem(filetype)
                
    def settmplnamelist(self, filetype):
        n=0
        self.ui.Template_Name_Box.clear()
        for tmpl in db.gettemplates(filetype):
            self.tmpllist[n*6:n*6+6] = list(tmpl[1:7])
            self.ui.Template_Name_Box.addItem(tmpl[7])
            n += 1

    # Action functions        
    def addfileaction(self):
        filename = self.addfile.getfilename()
        self.ui.Selected_File_Name.setText(filename)
        
    def okaction(self):
        doctitle = unicode(self.ui.document_title.text())
        project = self.selectedproject()
        doctype = self.selecteddoctype().upper()
        issue = "1"
        selectedtab = self.ui.Create_From_Tab.currentIndex()

        if selectedtab == 0:
            # Create from template
            tmplnamelist = self.selectedtemplate()
            createfromurl = self.link.const_docfileurl(tmplnamelist)
            filetype = tmplnamelist.pop(-1)
            create = True
        if selectedtab == 1:
            # Create from File
            addfilepath = unicode(self.ui.Selected_File_Name.text())
            filetype = addfilepath.rsplit('.')[-1]
            create = False
        if selectedtab == 2:
            # Create from existing Document
            basedocid = unicode(self.ui.Document_Id.text())
            basedocissue = unicode(self.ui.Issue.text())

            # Display error if file does not exist
            if not db.docexists(basedocid, basedocissue):
                QtGui.QMessageBox.critical(None, "Error","Document "+basedocid+\
                                           ", issue "+issue+" does not exists")
                return 
            else:
                # Construct url to based on document     
                filetype = db.getdocext(basedocid, issue)
                basedoclist = basedocid.split('-')
                basedoclist.extend([basedocissue, filetype])
                createfromurl = self.link.const_docfileurl(basedoclist) 
                create = True
                
        docnamelist = self.link.const_docnamelist(self.cat, project, doctype, \
                                                  issue, filetype)
        if create:
            self.doc.createdocument(createfromurl, docnamelist, doctitle)
        else:
            self.doc.adddocument(addfilepath, docnamelist, doctitle)
        self.close()

################################################################################
        
class addFileDialog(QtGui.QFileDialog):
    def __init__(self, parent=None):
        QtGui.QFileDialog.__init__(self, parent)

    def getfilename(self):
        self.setFilters(["Text (*.txt *.tex)", "Compressed (*.zip)", \
                         "Portable (*.pdf)"])
        self.setFilter("Text (*.txt *.tex)")
        return self.getOpenFileName(self, 'Select file to add',
                                    '/home', \
                                    "Supported (*.pdf *.txt *.tex *.zip)")
        
################################################################################

class documentInfoDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Document_Info_Dialog()
        self.ui.setupUi(self)
        self.addbuttons()

        # Connect buttons
        self.connect(self.ui.edit, QtCore.SIGNAL("clicked()"), \
                     self.savechanges)
        self.connect(self.ui.checkin, QtCore.SIGNAL("clicked()"), \
                     self.savechanges)
        self.connect(self.ui.commit, QtCore.SIGNAL("clicked()"), \
                     self.savechanges)
        self.connect(self.ui.save, QtCore.SIGNAL("clicked()"), \
                     self.savechanges)


    def addbuttons(self):
        self.ui.edit = self.ui.Document_Info_Confirm.addButton("Edit" , 3)
        self.ui.checkin = self.ui.Document_Info_Confirm.addButton("Check-in" , \
                                                                     3)
        self.ui.commit = self.ui.Document_Info_Confirm.addButton("Commit" , \
                                                                     3)
        self.ui.save = self.ui.Document_Info_Confirm.addButton("Save" , \
                                                                     3)

    def setdocinfo(self, docnamelist):
        """ Set document info. """
        info = db.getdocumentinfo(docnamelist)
        self.ui.state.setText(self.doc.getstate(docnamelist)[1])
        self.ui.document_id.setText(self.link.const_docid(docnamelist))
        self.ui.issue.setText(str(self.doc.getissueno(docnamelist)))
        self.ui.status.setText(info[9])
        self.ui.document_title.setText(info[7])
        self.ui.file_type.setText(info[6])
        self.ui.date.setText(info[8][0:19])
        self.ui.author.setText(info[10])

    def savechanges(self):
        """ Save changes. """
        if self.ui.document_title.isModified():
            print "check save"
        
