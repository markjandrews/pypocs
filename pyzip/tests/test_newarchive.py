from ctypes import *
from unittest import TestCase

from pyzip import api

class TestNewArchive(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_general_aes256(self):
        a = api.archive_write_new()
        self.assertEqual(api.archive_write_set_format_zip(a), 0)
        self.assertEqual(api.archive_write_add_filter_gzip(a), 0)
        self.assertEqual(api.archive_write_set_options(a, "zip:encryption=aes256".encode('latin-1')), 0)
        self.assertEqual(api.archive_write_set_passphrase(a, "password".encode('latin-1')), 0)

    def test_general_zipcrypt(self):
        a = api.archive_write_new()
        self.assertEqual(api.archive_write_set_format_zip(a), 0)
        self.assertEqual(api.archive_write_add_filter_gzip(a), 0)
        self.assertEqual(api.archive_write_set_options(a, "zip:encryption=zipcrypt".encode('latin-1')), 0)
        self.assertEqual(api.archive_write_set_passphrase(a, "password".encode('latin-1')), 0)

    def test_general_compressfile(self):
        AE_IFREG = 100000

        a = api.archive_write_new()
        self.assertEqual(api.archive_write_set_format_zip(a), 0)
        self.assertEqual(api.archive_write_add_filter_none(a), 0)
        self.assertEqual(api.archive_write_set_options(a, "zip:encryption=aes256".encode('latin-1')), 0)
        self.assertEqual(api.archive_write_set_passphrase(a, "password".encode('latin-1')), 0)

        self.assertEqual(api.archive_write_open_filename(a, 'test.zip'.encode('latin-1')), 0)

        entry = api.archive_entry_new()
        with open('test_newarchive.py', 'rb') as inf:
            data = inf.read()

        api.archive_entry_set_pathname(entry, 'fred/bob/file01.txt'.encode('latin-1'))

        api.archive_entry_set_filetype(entry, AE_IFREG)
        api.archive_entry_set_size(entry, len(data))
        # api.archive_entry_set_perm(entry, 644)

        self.assertEqual(api.archive_write_header(a, entry), 0)

        buf = (c_uint8 * len(data))()
        memmove(buf, data, len(data))
        buf_p = cast(buf, c_void_p)
        self.assertEqual(api.archive_write_data(a, buf_p, len(data)), len(data))

        self.assertEqual(api.archive_entry_free(entry), 0)
        self.assertEqual(api.archive_write_close(a), 0)
        self.assertEqual(api.archive_write_free(a), 0)
