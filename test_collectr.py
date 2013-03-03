# -*- coding: utf-8 -*-
"""
test_collectr
-------------

Some functions to test the collectr library.

:copyright: (c) 2013 Cory Benfield
:license: MIT License, for details see LICENSE.
"""
import unittest
import collectr
import subprocess
import mock


class CollectrTest(unittest.TestCase):
    """
    Tests for the collectr library.
    """
    def setUp(self):
        self.old_call = subprocess.call
        subprocess.call = mock.MagicMock(return_value=0)
        self.dir = collectr.StaticDir('test/fixtures/dirB')

    def tearDown(self):
        self.dir = None

        try:          # Delete the files if they exist, otherwise mask failure.
            self.old_call('rm -rf test/fixtures/dirB/css')
            self.old_call('rm -rf test/fixtures/dirB/js')
        except OSError:
            pass

    def test_enumerate_files(self):
        result = ['test/fixtures/dirA/css/css1.css',
                  'test/fixtures/dirA/css/css2.css',
                  'test/fixtures/dirA/js/script1.js',
                  'test/fixtures/dirA/js/script2.js']
        files = self.dir.enumerate_files('test/fixtures/dirA')
        self.assertEqual(files, result)

    def test_enumerate_files_with_filter(self):
        result = ['test/fixtures/dirB/img/img1.jpg',
                  'test/fixtures/dirB/img/img3.tiff']
        self.dir.ignore = ['.*\.png']
        files = self.dir.enumerate_files('test/fixtures/dirB')
        self.assertEqual(files, result)


if __name__ == '__main__':
    unittest.main()
