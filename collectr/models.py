# -*- coding: utf-8 -*-
"""
collectr.models
---------------

This module contains the main models used by collectr.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""


class StaticDir(object):
    """
    This class represents a single directory or directory tree of static files.
    This class can be created by the user, or used internally in collectr.

    :param directory: The root of the directory tree.
    """
    def __init__(self, directory):
        #: The root of the directory tree.
        self.directory = directory

        #: A string representing the location of static files that have yet to
        #: be minified. Files in this directory will be minified, and the
        #: minified versions will be saved to 'dir'.
        self.input_directory = None

        #: The minifier to use on CSS and/or Javascript files. May be a
        #: dictionary whose keys correspond to file extensions or a string. The
        #: string is considered a special case, and will be applied to both
        #: Javascript and CSS files.
        #: If the dictionary is used, the keys correspond to a command-line to
        #: run. This should be a python format string with two string
        #: variables, %{in}s and %{out}s. These refer to the input and output
        #: filename respectively.
        self.minifier = {'css': None, 'js': None}

        #: Whether to update all files, regardless of whether they have been
        #: changed.
        self.force_update = False

        #: Files to ignore. Should be a list of regular expressions. Everything
        #: that matches any of these regular expressions will be totally
        #: ignored. The regex will be applied to the relative path.
        self.ignore = []

        #: A dictionary of keys and values that correspond to the metadata that
        #: should be applied to the files. This metadata will be applied to
        #: _all_ the files found by this :class:`StaticDir <StaticDir>`.
        self.metadata = {}

    def update(self, bucket_name):
        """
        Connect to S3 and update the bucket with the static files from the
        directory.
        """
        # Non-destructive parts first.
        files = self.enumerate_files()
        conn = self.connect_s3()

        # Now that we know we have a connection, begin the destructive parts.
        files = self.minify_files(files)
        self.upload_files(files)
        return
