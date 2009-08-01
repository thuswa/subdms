#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Sat Aug  1 20:04:15 2009 on violator
# update count: 1393
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
import icondict
import frontend 
import lowlevel

from subdms import __version__
from aboutui import Ui_AboutDialog
from commitui import Ui_Commit_Dialog
from createdocumentui import Ui_New_Document_Dialog
from createprojui import Ui_New_Project_Dialog
from documentinfoui import Ui_Document_Info_Dialog
from helpviewui import helpView
from mainwindow import Ui_MainWindow

db = database.sqlitedb()

################################################################################

class ClientUi(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        self.state = frontend.docstate()
        self.conf = lowlevel.config()
        self.link = lowlevel.linkname()
        self.status = frontend.docstatus()
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.aboutdialog = aboutDialog()
        self.icons = icondict.iconDict()
        self.icons.addIconPath(self.conf.iconpath)
        self.helpview = helpView(self.conf.helppath, 'Subdms Documentation', \
                                 self.icons)

        self.commitdialog = commitDialog()
        self.projdialog = projectDialog()
        self.docdialog = documentDialog('P')
        self.tmpldialog = documentDialog('T')
        self.docinfodialog = documentInfoDialog()

        # Widget state lists
        self.noselectedlist = [False, False, False, False, False, False, \
                               False, False, False, False, False, False, \
                               True, True] 
        self.releasedlist = [True, True, True, False, False, False, \
                             False, True, False, False, False, False, \
                             True, True] 
        self.obsoletelist = [False, True, True, False, False, False, \
                             False, False, False, False, False, False, \
                             True, True] 
        self.preliminarylist = [False, True, True, True, True, True, \
                               True, True, True, True, True, True, \
                                False, False] 

        # start with most actions disabled
        self.disableactions(self.noselectedlist)
        
        # Set column width on document list 
        self.ui.documentlist.setColumnWidth(0, 40)
        self.ui.documentlist.setColumnWidth(1, 200)
        self.ui.documentlist.setColumnWidth(2, 420)
        self.ui.documentlist.setColumnWidth(3, 60)
        self.ui.documentlist.setColumnWidth(4, 60)
        self.ui.documentlist.setColumnWidth(5, 100)

        # Set column width on project list 
        self.ui.projectlist.setColumnWidth(0,  80)
        self.ui.projectlist.setColumnWidth(1, 340)
        self.ui.projectlist.setColumnWidth(2, 100)
        self.ui.projectlist.setColumnWidth(3, 160)
        self.ui.projectlist.setColumnWidth(4, 240)

        # Connect selection change signal to docselected action
        self.connect(self.ui.documentlist, \
                     QtCore.SIGNAL("itemSelectionChanged()"), self.docselected)

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
        self.connect(self.ui.actionList_Projects, \
                     QtCore.SIGNAL("activated()"), self.setprojectlist)

        # Tools menu
        self.connect(self.ui.actionDocument_Info, \
                     QtCore.SIGNAL("activated()"), self.showdocinfo)
        self.connect(self.ui.actionEdit_Document, \
                     QtCore.SIGNAL("activated()"), self.editdoc)
        self.connect(self.ui.actionView_Document, \
                     QtCore.SIGNAL("activated()"), self.viewdoc)
        self.connect(self.ui.actionCheck_in_Document, \
                     QtCore.SIGNAL("activated()"), self.checkindoc)
        self.connect(self.ui.actionCommit_Changes, \
                     QtCore.SIGNAL("activated()"), self.showcommitdialog)
        self.connect(self.ui.actionRelease_Document, \
                     QtCore.SIGNAL("activated()"), self.releasedoc)
        self.connect(self.ui.actionObsolete_Document, \
                     QtCore.SIGNAL("activated()"), self.obsoletedoc)

        # Help menu
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), \
                     self.showaboutdialog)
        self.connect(self.ui.actionDocumentation, \
                     QtCore.SIGNAL("activated()"), self.showhelpview)

        # Right-click menu = Tools
        self.connect(self.ui.documentlist, \
             QtCore.SIGNAL('customContextMenuRequested(const QPoint &)'), \
                     self.showrightclickmenu)

        # Connect buttons in document info dialog
        self.docinfodialog.connect(self.docinfodialog.ui.view, \
                                   QtCore.SIGNAL("clicked()"), self.viewdoc)
        self.docinfodialog.connect(self.docinfodialog.ui.edit, \
                                   QtCore.SIGNAL("clicked()"), self.editdoc)
        self.docinfodialog.connect(self.docinfodialog.ui.checkin, \
                                   QtCore.SIGNAL("clicked()"), self.checkindoc)
        self.docinfodialog.connect(self.docinfodialog.ui.commit, \
                                   QtCore.SIGNAL("clicked()"), \
                                   self.showcommitdialog)

    def docselected(self):
        docnamelist = self.getselecteddoc()
        if docnamelist:
            if self.status.isreleased(docnamelist):
                self.disableactions(self.releasedlist)
            if self.status.isobsolete(docnamelist):
                self.disableactions(self.obsoletelist)            
            if self.status.ispreliminary(docnamelist):
                self.disableactions(self.preliminarylist)

    def disableactions(self, statuslist):
        # Menu entries
        self.ui.actionNew_Issue.setEnabled(statuslist[0])
        self.ui.actionDocument_Info.setEnabled(statuslist[1])
        self.ui.actionView_Document.setEnabled(statuslist[2])
        self.ui.actionEdit_Document.setEnabled(statuslist[3])
        self.ui.actionCheck_in_Document.setEnabled(statuslist[4])
        self.ui.actionCommit_Changes.setEnabled(statuslist[5])
        self.ui.actionRelease_Document.setEnabled(statuslist[6])
        self.ui.actionObsolete_Document.setEnabled(statuslist[7])
        # Buttons in document info dialog
        self.docinfodialog.ui.edit.setEnabled(statuslist[8])
        self.docinfodialog.ui.checkin.setEnabled(statuslist[9])
        self.docinfodialog.ui.commit.setEnabled(statuslist[10])
        self.docinfodialog.ui.save.setEnabled(statuslist[11])
        # Fields in document info dialog 
        self.docinfodialog.ui.document_title.setReadOnly(statuslist[12])
        self.docinfodialog.ui.document_keywords.setReadOnly(statuslist[13])
         
    def showdocinfo(self):
        docnamelist = self.getselecteddoc()
        self.docinfodialog.show()
        self.docinfodialog.setdocinfo(docnamelist)
        self.docinfodialog.ui.historylist.clearContents()
        self.docinfodialog.ui.Info_tabs.setCurrentIndex(0)
        
    def showrightclickmenu(self):
        self.ui.menuTools.popup(QtGui.QCursor.pos())
        
    def showaboutdialog(self):
        """ Show about dialog. """
        self.aboutdialog.show()

    def showhelpview(self):
        """ Show documentation view. """
        self.helpview.show()

    def showdocdialog(self):
        """ Show create document. """        
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
        """ Show create template. """        
        self.tmpldialog.setprojlist()
        self.tmpldialog.setfiletypelist()
        self.tmpldialog.setdoctypelist(self.tmpldialog.selectedproject())
        self.tmpldialog.settmplnamelist(self.tmpldialog.selectedfiletype())
        self.tmpldialog.ui.Title_Label.setText("Template title:")
        self.tmpldialog.setWindowTitle("Create Template") 
        self.tmpldialog.show()

    def showcommitdialog(self):     
        """ Commit changes on document. """
        docnamelist = self.getselecteddoc()
        self.commitdialog.showdialog(docnamelist)

    def settemplatelist(self):
        """ List the existing templates. """
        self.setlist(db.getalltmpls())        
    def setdocumentlist(self):
        """ List the existing documents. """
        self.setlist(db.getalldocs())

    def setlist(self, docs):
        """ List the existing documents. """
        self.ui.documentlist.clearContents()
        n = 0
        for doc in docs:
            docnamelist = list(doc[1:7])
            state = QtGui.QTableWidgetItem(self.state.getstate(docnamelist)[0])
            docid = QtGui.QTableWidgetItem(self.link.const_docid(docnamelist))
            title = QtGui.QTableWidgetItem(doc[7].replace(u"\n" , u" || "))
            doctype = QtGui.QTableWidgetItem(doc[6])
            issue =  QtGui.QTableWidgetItem(doc[5])
            status = QtGui.QTableWidgetItem(doc[8])
            self.ui.documentlist.setItem(n, 0, state)
            self.ui.documentlist.setItem(n, 1, docid)
            self.ui.documentlist.setItem(n, 2, title)
            self.ui.documentlist.setItem(n, 3, doctype)
            self.ui.documentlist.setItem(n, 4, issue)
            self.ui.documentlist.setItem(n, 5, status)
            n += 1        

    def setprojectlist(self):
        """ List the existing projects. """
        self.ui.projectlist.clearContents()
        n = 0
        for proj in db.getallprojs():
            acronym = QtGui.QTableWidgetItem(proj[2])      
            description = QtGui.QTableWidgetItem(proj[3])      
            author = QtGui.QTableWidgetItem(proj[4])      
            date = QtGui.QTableWidgetItem(proj[5][0:19])
            doctypes = QtGui.QTableWidgetItem(proj[6])
            self.ui.projectlist.setItem(n, 0, acronym)
            self.ui.projectlist.setItem(n, 1, description) 
            self.ui.projectlist.setItem(n, 2, author)
            self.ui.projectlist.setItem(n, 3, date)
            self.ui.projectlist.setItem(n, 4, doctypes)
            n += 1        

    def getselecteddoc(self):
        """ Get the document selected in list. """
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
        """ Check-in document action. """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            message = self.doc.checkin(docnamelist)
            self.ui.statusbar.showMessage(message, 1500)

    def editdoc(self):
        """ Edit document action. """
        docnamelist = self.getselecteddoc()
        self.ui.statusbar.showMessage("Launching editor", 1500)
        self.doc.editdocument(docnamelist)

    def viewdoc(self):
        """ View document action. """
        docnamelist = self.getselecteddoc()
        self.ui.statusbar.showMessage("Launching viewer", 1500)
        self.doc.viewdocument(docnamelist)
            
    def releasedoc(self):     
        """ Release the document action. """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            confirm = QtGui.QMessageBox.question (None, \
                                            'Confirm status change', \
                                            'Really release this document?', \
                                            QtGui.QMessageBox.Yes, \
                                            QtGui.QMessageBox.No)
            if confirm:
                message = self.doc.release(docnamelist)
                self.ui.statusbar.showMessage(message, 1500)

    def obsoletedoc(self):     
        """ Obsolete the document action. """
        docnamelist = self.getselecteddoc()
        if docnamelist:
            confirm = QtGui.QMessageBox.question (None, \
                                            'Confirm status change', \
                                            'Really obsolete this document?', \
                                            QtGui.QMessageBox.Yes, \
                                            QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:                
                message = self.doc.obsolete(docnamelist)
                self.ui.statusbar.showMessage(message, 1500)

    def newissue(self):     
        """ Create a new issue. """
        docnamelist = self.getselecteddoc()
        if self.status.isnotreleased(docnamelist):
            QtGui.QMessageBox.critical(None, "Error",\
                                       "The selected document does not have "\
                                       "status \"released\". A new issue can "\
                                       "not be created unless the current "\
                                       "issue has first been released.")
        else:
            confirm = QtGui.QMessageBox.question (None, \
                                            'Confirm New Issue', \
                                            'Really create a new issue of ' \
                                            'this document?', \
                                            QtGui.QMessageBox.Yes, \
                                            QtGui.QMessageBox.No)

            if confirm == QtGui.QMessageBox.Yes:
                message = self.doc.newissue(docnamelist)
                self.ui.statusbar.showMessage(message, 1500)

################################################################################
            
class aboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.program_name.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML"
        "4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" "
        "/><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Tahoma\'; font-size:10pt;"
        "font-weight:600; font-style:italic;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
        "margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:"
        "\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\""
        "><span style=\" font-size:29pt; font-weight:600;\">Subdms</span>< "
        "span style=\" font-family:\'serif\'; font-size:15pt; font-weight:600;"
        "\"> "+__version__+"</span></p></body></html>")



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

        # Set defaults
        self.setcategorylist()
        self.setdoctypes()
        
    def setcategorylist(self):
        self.ui.Select_Category_Box.clear()
        self.ui.Select_Category_Box.addItem(self.conf.categories[0])
        self.ui.Select_Category_Box.setEnabled(False)

    def setdoctypes(self):
        self.ui.doctypes.setText(self.conf.doctypes)       
            
    def okaction(self):
        category = unicode(self.ui.Select_Category_Box.currentText())
        acronym = unicode(self.ui.project_acronym.text()).upper()
        name = unicode(self.ui.project_name.text())
        doctypes = unicode(self.ui.doctypes.text()).upper().\
                   replace(" ","").rsplit(",")

        if not acronym:
            QtGui.QMessageBox.critical(None, "Error", \
                                       "Project acronym field can not be " \
                                       "left empty.")
        elif db.projexists(category, acronym):
            QtGui.QMessageBox.critical(None, "Error", \
                                       "Project "+acronym+" already exists " \
                                       "in category "+category)
          
        else:
            self.proj.createproject(category, acronym, name, doctypes)
            self.close()

################################################################################
            
class documentDialog(QtGui.QDialog):
    def __init__(self, category, parent=None):
        self.doc = frontend.document()
        self.link = lowlevel.linkname()
        self.conf = lowlevel.config()
        self.addfile = addFileDialog(self.conf.getfilefilter())

        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_New_Document_Dialog()
        self.ui.setupUi(self)
        self.cat = category
        self.tmpllist = []
        self.setcategorylist()
        
        # Connect comboboxes and buttons
        self.connect(self.ui.Select_Project_Box, \
                     QtCore.SIGNAL("activated(const QString &)"),
                     self.setdoctypelist)
        self.connect(self.ui.File_Type_Box, \
                     QtCore.SIGNAL("activated(const QString &)"),
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
    def setcategorylist(self):
        self.ui.Select_Category_Box.clear()
        self.ui.Select_Category_Box.addItem(self.cat)
        self.ui.Select_Category_Box.setEnabled(False)
        
    def setprojlist(self):
        self.ui.Select_Project_Box.clear()
        if self.cat == "T":
            self.ui.Select_Project_Box.addItem("TMPL")
        else:
            for proj in db.getprojs():
                self.ui.Select_Project_Box.addItem(proj[0])
            
    def setdoctypelist(self, project):
        self.ui.Select_Type_Box.clear()
        for doctype in db.getdoctypes(self.cat, unicode(project)).split(","):
            self.ui.Select_Type_Box.addItem(doctype)

    def setfiletypelist(self):
        self.ui.File_Type_Box.clear()
        for filetype in self.conf.getsupportedfiletypes():
            if db.gettemplates(filetype):
                self.ui.File_Type_Box.addItem(filetype)
                
    def settmplnamelist(self, filetype):
        n=0
        self.ui.Template_Name_Box.clear()
        for tmpl in db.gettemplates(unicode(filetype)):
            self.tmpllist[n*6:n*6+6] = list(tmpl[1:7])
            self.ui.Template_Name_Box.addItem(tmpl[7])
            n += 1

    # Action functions        
    def addfileaction(self):
        filename = self.addfile.getfilename()
        self.ui.Selected_File_Name.setText(filename)
        
    def okaction(self):
        doctitle = unicode(self.ui.document_title.toPlainText())
        dockeywords = unicode(self.ui.document_keywords.toPlainText())
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
            self.doc.createdocument(createfromurl, docnamelist, doctitle, \
                                    dockeywords)
        else:
            self.doc.adddocument(addfilepath, docnamelist, doctitle, \
                                 dockeywords)
        self.close()

################################################################################
        
class addFileDialog(QtGui.QFileDialog):
    def __init__(self, filterstr, parent=None):
        """ initialize the File dialog
        filterstr is the string defining the file types that are supported."""  
        self.filter = filterstr
        QtGui.QFileDialog.__init__(self, parent)
        
    def getfilename(self):
        return self.getOpenFileName(self, 'Select file to add',
                                    '/home', self.filter)

        
################################################################################

class documentInfoDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        self.state = frontend.docstate()
        self.link = lowlevel.linkname()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Document_Info_Dialog()
        self.ui.setupUi(self)

        # Set dimensions of history list
        self.ui.historylist.verticalHeader().hide()
        self.ui.historylist.setColumnWidth(0, 60)
        self.ui.historylist.setColumnWidth(1, 300)
        self.ui.historylist.setColumnWidth(2, 90)
        self.ui.historylist.setColumnWidth(3, 160)        

        # add the buttons
        self.addbuttons()

        # Connect save button
        # the rest are set in main window class
        self.connect(self.ui.save, QtCore.SIGNAL("clicked()"), \
                     self.savechanges)

        # Set change tab action 
        self.connect(self.ui.Info_tabs, \
                     QtCore.SIGNAL("currentChanged(int)"), \
                     self.changedtab)

    def addbuttons(self):
        self.ui.view = self.ui.Document_Info_Confirm.addButton("View" , 3)
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
        self.ui.state.setText(self.state.getstate(docnamelist)[1])
        self.ui.document_id.setText(self.link.const_docid(docnamelist))
        self.ui.issue.setText(str(self.doc.getissueno(docnamelist)))
        self.ui.status.setText(info[8])
        self.ui.document_title.setPlainText(info[7])
        self.ui.document_keywords.setPlainText(info[10])
        self.ui.file_type.setText(info[6])
        self.ui.creation_date.setText(info[11][0:19])
        self.ui.release_date.setText(info[12][0:19])
        self.ui.obsolete_date.setText(info[13][0:19])
        self.ui.author.setText(info[9])

    def savechanges(self):
        """ Save changes. """
        #if self.ui.document_title.textChanged():
        doctitle = unicode(self.ui.document_title.toPlainText())
        dockeywords = unicode(self.ui.document_keywords.toPlainText())
        docid = unicode(self.ui.document_id.text())
        issue = unicode(self.ui.issue.text())
        filetype = unicode(self.ui.file_type.text())
        doclist = docid.split('-')
        doclist.extend([issue, filetype])
        self.doc.changetitle(doclist, doctitle) 
        self.doc.changekeywords(doclist, dockeywords) 
        
    def changedtab(self, selectedtab):
        """ Changed tab. """
        if selectedtab == 0:  #General 
            pass
        elif selectedtab == 1: #History
            self.sethistory()

    def sethistory(self):
        """ Set revision history list. """
        docid = unicode(self.ui.document_id.text())
        issue = unicode(self.ui.issue.text())
        docnamelist = self.link.deconst_docfname(docid)
        docnamelist.append(issue) 
        docrevlist = db.getdocrev(docnamelist)
        docrevlist.reverse()
        n = 0
        for docrev in docrevlist:
            rvn = QtGui.QTableWidgetItem(str(docrev[0]))
            log_message = QtGui.QTableWidgetItem(docrev[8])
            author = QtGui.QTableWidgetItem(docrev[7])
            revdate = QtGui.QTableWidgetItem(docrev[6][0:19])
            self.ui.historylist.setItem(n, 0, rvn) 
            self.ui.historylist.setItem(n, 1, log_message)
            self.ui.historylist.setItem(n, 2, author)
            self.ui.historylist.setItem(n, 3, revdate)        
            n += 1
    
################################################################################

class commitDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        self.doc = frontend.document()
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Commit_Dialog()
        self.ui.setupUi(self)
        self.doclist = []
        self.connect(self.ui.Commit_Changes_Confirm, \
                     QtCore.SIGNAL("accepted()"), self.okaction)

    def showdialog(self, docnamelist):
        self.doclist = docnamelist
        self.show()
        
    def okaction(self):
        dockeywords = unicode(self.ui.commit_message.toPlainText())
        self.doc.commit(self.doclist, dockeywords)
        self.close()

