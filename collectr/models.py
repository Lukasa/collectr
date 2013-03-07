# -*- coding: utf-8 -*-
"""
collectr.models
---------------

This module contains the main models used by collectr.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""
from .utils import (tree_walk, match_regexes, move_path, minified_filename,
                    get_extension, default_minifier)
from .exceptions import MinifierError
import re
import subprocess
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key


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
        #: variables, {in_name} and {out_name}. These refer to the input and
        #: output filename respectively. The string must be able to have
        #: .format() called on it.
        self.minifier = default_minifier()

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

        :param bucket_name: The name of the S3 bucket to upload to.
        """
        self.minify_files()
        files = self.enumerate_files(self.directory)
        conn = self.connect_s3()
        self.upload_files(files, bucket_name, conn)
        return

    def enumerate_files(self, directory):
        """
        Enumerate all the files beneath a directory. Walks into all
        directories except for those created by version control.

        :param directory: The root of the tree.
        """
        files = tree_walk(directory)

        # Ignore some files.
        files = self.filter_files(files)

        return files

    def filter_files(self, files):
        """
        Given a list of files, remove any that match any of a list of regular
        expressions.
        """
        tests = [re.compile(x) for x in self.ignore]

        # Bail early if we don't have any regexes to match.
        if tests:
            # Remove files that are matched by regexes.
            files = [name for name in files if not match_regexes(tests, name)]

        return files

    def minify_files(self):
        """
        Takes all the files either in the main directory or the input directory
        and minifies them. If the files came from the input directory, moves
        them to the main directory.
        """
        if self.input_directory:
            files = self.enumerate_files(self.input_directory)
        else:
            files = self.enumerate_files(self.directory)

        # Strings are a special case: apply that special case.
        if isinstance(self.minifier, basestring):
            minifier = {'css': self.minifier, 'js': self.minifier}
        else:
            minifier = self.minifier

        # For each file, if its extension has a minifier associated with it,
        # apply it.
        for name in files:
            try:
                command = minifier[get_extension(name)]
                command = command.format(in_name=name,
                                         out_name=self.get_output_name(name))

                rc = subprocess.call(command, shell=True)

                if rc != 0:
                    raise MinifierError("Error occurred during minification.")

            except KeyError:
                # If there's no minifier command, don't touch it.
                continue

        return

    def get_output_name(self, input_filename):
        """
        When minifying a file, determine its output filename. This depends on
        whether it's being copied to a new directory.
        """
        if self.input_directory:
            filename = move_path(self.input_directory,
                                 self.directory,
                                 input_filename)
            filename = minified_filename(filename)
        else:
            filename = minified_filename(input_filename)

        return filename

    def connect_s3(self):
        """
        Connect to S3. Returns the boto connection object.
        """
        return S3Connection()

    def upload_files(self, files, bucket_name, connection):
        """
        Given a list of files, an Amazon S3 bucket and a connection, uploads
        the files to the bucket. If the bucket doesn't exist, creates it.
        """
        # First get the bucket. If it exists, great. If not, create it.
        try:
            bucket = connection.get_bucket(bucket_name)
        except S3ResponseError:
            bucket = connection.create_bucket(bucket_name)

        # For each file, create an S3 key and upload the data. Then, set the
        # metadata.
        for path in files:
            key = self.find_or_create_key(path)
            key.set_contents_from_filename(path)

            for metakey, metavalue in self.metadata.iteritems():
                key.set_metadata(metakey, metavalue)

            # Set the visibility to public-read.
            key.set_acl('public-read')

        # All done.
        return

    def apply_metadata(self, key):
        """
        Apply any expected metadata to an S3 key. If the value is a dict, the
        key is treated as a regular expression that must match the file path.
        Otherwise, the key and value are applied to all keys.
        """
        for metakey, metavalue in self.metadata.iteritems():

            # If the value is a dict and the regex matches, apply all the key-
            # value pairs.
            if isinstance(metavalue, dict) and re.search(metakey, key.key):
                for newkey, newvalue in metavalue.iteritems():
                    key.set_metadata(newkey, newvalue)

            # Otherwise, always apply the key and value.
            elif not isinstance(metavalue, dict):
                key.set_metadata(metakey, metavalue)

        return

    def find_or_create_key(self, path, bucket):
        """
        For a given file, checks whether it's in the S3 bucket. If it is,
        returns the key object corresponding to it. If not, creates a new key
        and returns it.
        """
        name = self.key_name_from_path(path)
        key = bucket.lookup(name)

        if not key:
            key = Key(bucket)
            key.key = name

        return key

    def key_name_from_path(self, path):
        """
        Get the name of an S3 key from the path on the filesystem.
        """
        if self.directory[-1] != '/':
            temp_directory = self.directory + '/'
        else:
            temp_directory = self.directory

        return path.replace(temp_directory, '', 1)
