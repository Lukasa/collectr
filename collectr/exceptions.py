# -*- coding: utf-8 -*-
"""
collectr.exceptions
-------------------

This module contains any exceptions raised by collectr.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, see LICENSE for details.

"""
import subprocess


class MinifierError(subprocess.CalledProcessError):
    """
    An error encountered during execution of the minifier.
    """
