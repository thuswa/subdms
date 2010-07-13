#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# $Id$
# Last modified Wed Jul  7 20:51:13 2010 on stalker
# update count: 102
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

from svn import fs, repos, core

# from . import lowlevel # Python 3.X
import lowlevel

conf = lowlevel.config()
link = lowlevel.linkname()

def propset(docnamelist, propname, propvalue):
    """
    Own-rolled propset function that operates directly on the repo
    However it requires direct filesystem access to the repo.
    """

    # Get repository object
    repository = repos.open(conf.repopath) 

    # Get repo filesystem pointer
    fs_ptr = repos.fs(repository)
    
    # Get youngest revision
    youngest_revision_number = fs.youngest_rev(fs_ptr)

    # begin transaction
    txn = fs.begin_txn(fs_ptr, youngest_revision_number)
    txn_root = fs.txn_root(txn)

    # change property on node
    fs.change_node_prop(txn_root, link.const_docinrepopath(docnamelist), \
                        propname, propvalue)
    fs.commit_txn(txn)


