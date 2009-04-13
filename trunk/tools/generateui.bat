@echo off
REM $Id: generateui 206 2009-03-19 23:29:29Z albert.thuswaldner $
REM Last modified Mon Apr 13 16:41:50 2009 on violator
REM Update count: 107
REM
REM Created 2009-03-04, Albert Thuswaldner

pyuic4 ../ui/about.ui > ../subdms/aboutui.py
pyuic4 ../ui/createdocument.ui > ../subdms/createdocumentui.py
pyuic4 ../ui/createproj.ui > ../subdms/createprojui.py
pyuic4 ../ui/documentinfo.ui > ../subdms/documentinfoui.py
pyuic4 ../ui/mainwindow.ui > ../subdms/mainwindow.py
