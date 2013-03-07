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

    def test_minifier_works(self):
        # Set up directory.
        self.dir.input_directory = 'test/fixtures/dirA'
        self.dir.minifier = {'js': 'yuicompressor -o {out_name} {in_name}',
                             'css': 'yuicompressor -o {out_name} {in_name}'}
        files = [('test/fixtures/dirA/css/css1.css', 'test/fixtures/dirB/css/css1-min.css'),
                 ('test/fixtures/dirA/css/css2.css', 'test/fixtures/dirB/css/css2-min.css'),
                 ('test/fixtures/dirA/js/script1.js', 'test/fixtures/dirB/js/script1-min.js'),
                 ('test/fixtures/dirA/js/script2.js', 'test/fixtures/dirB/js/script2-min.js')]

        self.dir.minify_files()

        for infile, outfile in files:
            command_line = 'yuicompressor -o {out_name} {in_name}'.format(
                                                              out_name=outfile,
                                                              in_name=infile)
            subprocess.call.assert_any_call(command_line, shell=True)

    def test_metadata_application(self):
        # Set up some metadata.
        self.dir.metadata = {'.*\.png': {'Key1': 'Val1',
                                         'Key2': 'Val2'},
                             'Key3': 'Val3'}

        # First, test something that matches a regex.
        key = mock.MagicMock(key='test.png')
        self.dir.apply_metadata(key)
        key.set_metadata.assert_any_call('Key1', 'Val1')
        key.set_metadata.assert_any_call('Key2', 'Val2')
        key.set_metadata_assert_any_call('Key3', 'Val3')

        # Then test one that doesn't.
        key = mock.MagicMock(key='test.jpg')
        self.dir.apply_metadata(key)
        key.set_metadata.assert_called_once_with('Key3', 'Val3')

    def test_key_name_from_path(self):
        path = 'test/fixtures/dirB/dir/notherdir/name.extension'
        expected_result = 'dir/notherdir/name.extension'
        result = self.dir.key_name_from_path(path)
        self.assertEqual(result, expected_result)

    @mock.patch('boto.s3.key.Key')
    def test_find_or_create_key(self, mock_key):
        # Set up.
        instance = mock_key.return_value
        instance.key = 'test_key'
        bucket = mock.MagicMock()
        bucket.lookup.return_value = None

        # First, test when we can't find the key.
        result = self.dir.find_or_create_key('/test', bucket)
        bucket.lookup.assert_called_once_with('/test')
        self.assertEqual(result.key, '/test')

        # Next, test when we can.
        bucket.lookup.return_value = mock.MagicMock()
        result = self.dir.find_or_create_key('/test', bucket)
        bucket.lookup.assert_called_with('/test')
        self.assertEqual(result.key, '/test')


if __name__ == '__main__':
    unittest.main()
