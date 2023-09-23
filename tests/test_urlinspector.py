from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from cli.urlinspector import URLInspector


class TestURLInspector(unittest.TestCase):
    def setUp(self):

        self.temp_dir = tempfile.mkdtemp()
        self.valid_url = 'https://example.com'
        self.invalid_url = 'invalid-url'
        self.inspector = None

    def tearDown(self):

        shutil.rmtree(self.temp_dir)

    def test_valid_url(self):
        self.inspector = URLInspector(self.valid_url)
        self.assertEqual(self.inspector.url, self.valid_url)

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            self.inspector = URLInspector(self.invalid_url)

    def test_check_status_code(self):
        self.inspector = URLInspector(self.valid_url)
        status_code = self.inspector.check_status_code()
        self.assertEqual(status_code, 200)

    def test_check_content_length(self):
        self.inspector = URLInspector(self.valid_url)
        content_length = self.inspector.check_content_length()
        self.assertGreater(content_length, 0)

    def test_check_title(self):
        self.inspector = URLInspector(self.valid_url)
        title = self.inspector.check_title()
        self.assertTrue(title.startswith('<title>'))

    def test_check_word_in_body(self):
        self.inspector = URLInspector(self.valid_url)
        word_present = self.inspector.check_word_in_body('Example')
        self.assertTrue(word_present)

    def test_check_js_files(self):
        self.inspector = URLInspector(self.valid_url)
        js_hashes = self.inspector.check_js_files()
        self.assertTrue(js_hashes)

    def test_create_save_directory_custom(self):
        custom_dir = os.path.join(self.temp_dir, 'custom_dir')
        self.inspector = URLInspector(self.valid_url)
        save_dir = self.inspector.create_save_directory(
            custom_save_directory=custom_dir,
        )
        self.assertEqual(save_dir, custom_dir)
        self.assertTrue(os.path.exists(custom_dir))

    def test_create_save_directory_default(self):
        self.inspector = URLInspector(self.valid_url)
        save_dir = self.inspector.create_save_directory()
        expected_dir = os.path.join(
            self.inspector.INSPECTOR_DIR, self.inspector.JS_FILES_DIR, 'example.com',
        )
        self.assertEqual(save_dir, expected_dir)
        self.assertTrue(os.path.exists(expected_dir))


if __name__ == '__main__':
    unittest.main()
