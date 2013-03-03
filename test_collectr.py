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


class CollectrTest(unittest.TestCase):
    """
    Tests for the collectr library.
    """
    def setUp(self):
        self.dir = collectr.StaticDir('test/fixtures/dirB')

    def test_enumerate_files(self):
        result = ['test/fixtures/dirA/css/css1.css',
                  'test/fixtures/dirA/css/css2.css',
                  'test/fixtures/dirA/js/script1.js',
                  'test/fixtures/dirA/js/script2.js']
        files = self.dir.enumerate_files('test/fixtures/dirA')
        self.assertEqual(files, result)


if __name__ == '__main__':
    unittest.main()
