#!/usr/bin/env python
# $Id$
# Last modified Fri Mar  6 12:58:31 2009 on havoc
# update count: 53
# -*- coding:  utf-8 -*-

from svn import fs, repos, core

def propset(docfileurl, propname, propvalue):
    # Get repository object
    repository = repos.open(root_path) 

    # Get repo filesystem pointer
    fs_ptr = repos.fs(repository)
    
    # Get youngest revision
    youngest_revision_number = fs.youngest_rev(fs_ptr)

    # begin transaction
    txn = fs.begin_txn(fs_ptr, youngest_revision)
    txn_root = fs.txn_root(txn)

    # change property on node
    fs.change_node_prop(txn_root, docfileurl, propname, propvalue)
    
