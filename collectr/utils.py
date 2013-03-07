# -*- coding: utf-8 -*-
"""
collectr.utils
--------------

This module implements utility functions and holds utility data for collectr.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""
import os
import time

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
            files.append(os.path.join(dirpath, name))

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

    return path.replace(current_dir, new_dir, 1)


def minified_filename(path):
    """
    Given a path, returns a new path with the filename changed to a minified
    form, e.g. test.css -> test-min.css
    """
    name, extension = os.path.splitext(path)
    name += "-min"
    return name + extension


def get_extension(path):
    """
    Given a path, returns the extension, excluding the dot, e.g. test.css ->
    css.
    """
    _, extension = os.path.splitext(path)
    return extension[1:]


def default_minifier():
    """
    Determine the default minifier dict.
    """
    # TODO: Come back and generalise this.
    return 'yuicompressor -o {out_name} {in_name}'


def should_update_key(key, path):
    """
    Given a key and its associated file, determine whether it should be
    updated.
    """
    # First, if there's no modification date, it must be new.
    if not key.last_modified:
        return True

    key_time = time.strptime(key.last_modified,
                             "%a, %d %b %Y %H:%M:%S %Z")
    local_time = time.gmtime(os.path.getmtime(path))

    return key_time == local_time
