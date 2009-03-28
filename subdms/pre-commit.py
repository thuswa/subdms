#!/usr/bin/python
# $Id$
# Last modified Sat Mar 28 20:15:06 2009 on violator
# update count: 39
" Example Subversion pre-commit hook. "

def command_output(cmd):
    " Capture a command's standard output. "
    import subprocess
    return subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE).communicate()[0]

#def files_changed(look_cmd):
# """ List the files added or updated by this transaction.
#
#"svnlook changed" gives output like:
# U trunk/file1.cpp
# A trunk/file2.cpp
# """
# def filename(line):
# return line[4:]
# def added_or_updated(line):
# return line and line[0] in ("A", "U")
# return [
# filename(line)
# for line in command_output(look_cmd % "changed").split("\n")
# if added_or_updated(line)]
#
#def file_contents(filename, look_cmd):
# " Return a file's contents for this transaction. "
# return command_output(
# "%s %s" % (look_cmd % "cat", filename))
#
def main():
    usage = """usage: %prog REPOS TXN
    #
    #Run pre-commit options on a repository transaction."""
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--revision",
                      help="Test mode. TXN actually refers to a revision.",
                      action="store_true", default=False)
    # errors = 0
    # try:
    (opts, (repos, txn_or_rvn)) = parser.parse_args()
    look_opt = ("--transaction", "--revision")[opts.revision]
    look_cmd = "/usr/bin/svnlook %s %s %s %s > /home/thuswa/svnproj/log.txt" % ("%s", repos, look_opt, txn_or_rvn)
## files_changed(look_cmd)
    # print txn_or_rvnome/thuswa/svnproj/l
    # print look_cmd
    # command_output(look_cmd % "log > /home/thuswa/svnproj/log.txt")
    # except:
    print look_cmd
    command_output(look_cmd % "log")
    # parser.print_help()
    # errors += 1
    # return errors
    #
if __name__ == "__main__":
    import sys
    sys.exit(main())

