# -*- coding: utf-8 -*-
"""
collectr.api
------------

This module implements the public-facing portion of the collectr API.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""

from .models import StaticDir


def update(dir, bucket):
    """
    Updates an S3 bucket with the contents of a directory tree. Mirrors the
    tree into the S3 bucket. Returns nothing.

    :param dir: the root of the directory tree.
    :param bucket: the name of the S3 bucket to use.
    """
    raise NotImplemented("Not yet implemented.")
