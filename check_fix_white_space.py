#!/usr/bin/env python3

#
# Script to fix whithespace errors in files
# All trailing white space are removed
# TAB are replace by spaces
#
import glob
import sys

file_patterns_tab_width = {"**/*.Tc*": 4,
                           "**/*.py":  4,
                           "**/*.sh":  8}
def fix_white_space(debug, fix_files):
    """
    Checks the Twincat source code for white space:
    TAB should not be used
    Trailing SPACE shoulf not be there.
    :return: A dictionary of white-space-damaged files
    """
    incorrect_files = dict()
    for file_path, tab_width in file_patterns_tab_width.items():
        found_files = glob.glob(file_path, recursive=True)
        #if not found_files:
        #    raise IOError("ERROR: No files of type {} found".format(file_path))

        for pathname in found_files:
            dirty = False
            new_lines = []
            if debug >= 1:
                print("tab_with=%d pathname=%s" % (tab_width, pathname))
            file = open(pathname, 'r', newline='', encoding="iso-8859-1")
            lines = file.readlines()
            file.close()
            for old_line in lines:
                had_crlf = 0
                this_line_dirty = False
                if old_line.endswith('\r\n'):
                    had_crlf = 2 # Both CR and LF
                elif old_line.endswith('\n'):
                    had_crlf = 1 # LF
                # Convert all TAB into SPACE
                new_line = old_line.expandtabs(tabsize=tab_width)
                # Strip of all trailing white space, including the CRLF
                new_line = new_line.rstrip("\r\n ")
                if had_crlf == 2:
                    new_line = new_line + '\r\n'
                elif had_crlf == 1:
                    new_line = new_line + '\n'

                if len(new_line) != len(old_line):
                    dirty = True
                    this_line_dirty = True
                new_lines.append(new_line)
                if this_line_dirty:
                   if debug >= 2:
                       print("had_crlf=%d" % had_crlf)
                       print("old_line=%s" % old_line)
                       print("new_line=%s" % new_line)
            # end of loop of all line in one file
            if debug >= 1:
                print("pathname=%s dirty=%d" % (pathname, dirty))
            if dirty:
                incorrect_files[pathname] = True
                if fix_files:
                    file = open(pathname, 'w', newline='', encoding="iso-8859-1")
                    file.writelines(new_lines)
                    file.close()

    return incorrect_files


if __name__ == "__main__":
    try:
        argc = len(sys.argv)
        arg_idx = 1
        debug = 0
        fix_files = False
        while arg_idx < argc:
            if sys.argv[arg_idx] == "--fix":
                fix_files = True
            elif sys.argv[arg_idx] == "--debug":
                debug = debug + 1
            else:
                print("%s : [--fix|--debug]" % sys.argv[0])
                exit(2)
            arg_idx = arg_idx + 1
        incorrect_files = fix_white_space(debug, fix_files)
        if not fix_files:
            for file in incorrect_files:
                print("ERROR: '{}' has white space damage".format(file))
        if incorrect_files:
            print('run %s --fix' % sys.argv[0])
            exit(1)
    except IOError as e:
        print(e)  # Likely no files found
        exit(2)
