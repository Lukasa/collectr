# -*- coding: utf-8 -*-
"""
collectr.utils
--------------

This module implements utility functions and holds utility data for collectr.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""
import os

# Directories created by version control software.
VCS_DIRS = ['.git', '.svn', '.hg']


def tree_walk(directory):
    """
    Recursively walk a directory tree. Returns a list of files in the
    tree. Does not walk down folders created by version control.
    """
    files = []

    for dirpath, subdirs, filenames in os.walk(directory):
        for name in filenames:
            files.append(os.path.join(name, dirpath))

        # Ignore version control directories.
        for vcs_dir in VCS_DIRS:
            if vcs_dir in subdirs:
                subdirs.remove(vcs_dir)

    return files


def match_regexes(regexes, string):
    """
    Given a string, determine if it matches any of a list of regular
    expressions. Returns True if it does, False if it doesn't.
    """
    match = [regex.search(string) for regex in regexes if regex.search(string)]

    if match:
        return True
    else:
        return False
