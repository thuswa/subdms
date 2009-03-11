#!/usr/bin/env python
# $Id$
# Last modified Wed Mar 11 19:42:30 2009 on violator
# update count: 94
# -*- coding:  utf-8 -*-

from svn import fs, repos, core

import lowlib

conf = lowlib.dmsconfig()
docs = lowlib.docname()

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
    fs.change_node_prop(txn_root, docs.const_docinrepopath(docnamelist), \
                        propname, propvalue)
    fs.commit_txn(txn)


