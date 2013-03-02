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


def move_path(current_dir, new_dir, path):
    """
    Move a path from one directory to another. Given the directory the path is
    currently in, moves it to be in the second. The path below the given
    directory level remains the same.
    """
    if current_dir[-1] != '/':
        current_dir += '/'
    if new_dir[-1] != '/':
        new_dir += '/'

    return string.replace(path, current_dir, new_dir, 1)


def minified_filename(path):
    """
    Given a path, returns a new path with the filename changed to a minified
    form, e.g. test.css -> test-min.css
    """
    name, extension = os.path.splittext(path)
    name += "-min"
    return name + extension


def get_extension(path):
    """
    Given a path, returns the extension, excluding the dot, e.g. test.css ->
    css.
    """
    _, extension = os.path.splittext(path)
    return path[1:]
