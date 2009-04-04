@echo off
REM $Id: generateui 206 2009-03-19 23:29:29Z albert.thuswaldner $
REM Last modified Fri Mar 20 00:29:15 2009 on violator
REM Update count: 106
REM
REM Created 2009-03-04, Albert Thuswaldner

pyuic4 ../ui/about.ui > ../subdms/aboutui.py
pyuic4 ../ui/createdocument.ui > ../subdms/createdocumentui.py
pyuic4 ../ui/createproj.ui > ../subdms/createprojui.py
pyuic4 ../ui/mainwindow.ui > ../subdms/mainwindow.py
