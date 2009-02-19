#!/bin/sh

# PRE-COMMIT HOOK
#
# The pre-commit hook is invoked before a Subversion txn is
# committed.  Subversion runs this hook by invoking a program
# (script, executable, binary, etc.) named 'pre-commit' (for which
# this file is a template), with the following ordered arguments:
#
#   [1] REPOS-PATH   (the path to this repository)
#   [2] TXN-NAME     (the name of the txn about to be committed)
#
# The default working directory for the invocation is undefined, so
# the program should set one explicitly if it cares.
#
# If the hook program exits with success, the txn is committed; but
# if it exits with failure (non-zero), the txn is aborted, no commit
# takes place, and STDERR is returned to the client.   The hook
# program can use the 'svnlook' utility to help it examine the txn.
#
# On a Unix system, the normal procedure is to have 'pre-commit'
# invoke other programs to do the real work, though it may do the
# work itself too.
#
#   ***  NOTE: THE HOOK PROGRAM MUST NOT MODIFY THE TXN, EXCEPT  ***
#   ***  FOR REVISION PROPERTIES (like svn:log or svn:author).   ***
#
#   This is why we recommend using the read-only 'svnlook' utility.
#   In the future, Subversion may enforce the rule that pre-commit
#   hooks should not modify the versioned data in txns, or else come
#   up with a mechanism to make it safe to do so (by informing the
#   committing client of the changes).  However, right now neither
#   mechanism is implemented, so hook writers just have to be careful.
#
# Note that 'pre-commit' must be executable by the user(s) who will
# invoke it (typically the user httpd runs as), and that user must
# have filesystem-level permission to access the repository.
#
# On a Windows system, you should name the hook program
# 'pre-commit.bat' or 'pre-commit.exe',
# but the basic idea is the same.
#
# The hook program typically does not inherit the environment of
# its parent process.  For example, a common problem is for the
# PATH environment variable to not be set to its usual value, so
# that subprograms fail to launch unless invoked via absolute path.
# If you're having unexpected problems with a hook program, the
# culprit may be unusual (or missing) environment variables.
# 
# Here is an example hook script, for a Unix /bin/sh interpreter.
# For more examples and pre-written hooks, see those in
# the Subversion repository at
# http://svn.collab.net/repos/svn/trunk/tools/hook-scripts/ and
# http://svn.collab.net/repos/svn/trunk/contrib/hook-scripts/


REPOS="$1"
TXN="$2"

#/bin/echo $REPOS > /home/thuswa/repo.txt

# Make sure that the log message contains some text.
SVNLOOK=/usr/bin/svnlook
/bin/echo `$SVNLOOK log -t "$TXN" "$REPOS"` >>  /home/thuswa/svnproj/log.txt
/bin/echo `$SVNLOOK cat -t "$TXN" "$REPOS"` >>  /home/thuswa/svnproj/cat.txt
/bin/echo `$SVNLOOK diff -t "$TXN" "$REPOS"` >>  /home/thuswa/svnproj/diff.txt
/bin/echo `$SVNLOOK changed -t "$TXN" "$REPOS"` >>  /home/thuswa/svnproj/changed.txt
/bin/echo `$SVNLOOK info -t "$TXN" "$REPOS"` >>  /home/thuswa/svnproj/info.txt
/bin/echo $REPOS >>  /home/thuswa/svnproj/repo.txt
/bin/echo $TXN >>  /home/thuswa/svnproj/txn.txt
 
#   grep "[a-zA-Z0-9]" > /dev/null || exit 1

# Check that the author of this commit has the rights to perform
# the commit on the files and directories being modified.
#commit-access-control.pl "$REPOS" "$TXN" commit-access-control.cfg || exit 1

# All checks passed, so allow the commit.
exit 0
