from ctypes import *
from unittest import TestCase

from pyzip import api


class TestIso9660(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_general_newiso(self):
        AE_IFREG = 100000

        a = api.archive_write_new()
        self.assertEqual(api.archive_write_set_format_iso9660(a), 0)
        self.assertEqual(api.archive_write_add_filter_none(a), 0)
        self.assertEqual(api.archive_write_open_filename(a, 'test.iso'.encode('latin-1')), 0)

        with open('test_iso9660.py', 'rb') as inf:
            data = inf.read()

        entry = api.archive_entry_new()
        api.archive_entry_set_pathname(entry, 'fred/bob/file01.txt'.encode('latin-1'))
        api.archive_entry_set_filetype(entry, AE_IFREG)
        api.archive_entry_set_size(entry, len(data))
        self.assertEqual(api.archive_write_header(a, entry), 0)

        buf = (c_uint8 * len(data))()
        memmove(buf, data, len(data))
        buf_p = cast(buf, c_void_p)
        self.assertEqual(api.archive_write_data(a, buf_p, len(data)), len(data))

        self.assertEqual(api.archive_entry_free(entry), 0)
        self.assertEqual(api.archive_write_close(a), 0)
        self.assertEqual(api.archive_write_free(a), 0)
