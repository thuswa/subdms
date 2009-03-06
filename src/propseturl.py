#!/usr/bin/env python
# $Id$
# Last modified Fri Mar  6 23:17:47 2009 on violator
# update count: 81
# -*- coding:  utf-8 -*-

from svn import fs, repos, core
import string
import config

conf = config.dmsconfig()

def propset(docnamelist, propname, propvalue):
    """
    Own-rolled propset function that operates directly on te repo
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

    path=__const_docfileurl(docnamelist).split(conf.repopath)[1]
    # change property on node
    fs.change_node_prop(txn_root,path,propname, propvalue)
    fs.commit_txn(txn)


def __const_docname(docnamelist):
   """ Construct the document file name. """
   return string.join(docnamelist[:-1],'-')+'.'+docnamelist[-1:].pop()

def __const_docurl(docnamelist):
   """ Construct the document url. """
   docurllist=[conf.trunkurl]
   docurllist.extend(docnamelist[:-1])
   return string.join(docurllist, '/')
    
def __const_docfileurl(docnamelist):
   """ Construct the document file url. """
   return string.join([__const_docurl(docnamelist), \
                       __const_docname(docnamelist)], '/')
