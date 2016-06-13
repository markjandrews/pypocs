import os
from ctypes import *

SCRIPT_DIR = os.path.dirname(__file__)

dll = cdll.LoadLibrary(os.path.join(SCRIPT_DIR, 'native', 'archive.dll'))

archive_write_new = dll.archive_write_new
archive_write_new.argtypes = []
archive_write_new.restype = c_void_p

archive_write_set_format_zip = dll.archive_write_set_format_zip
archive_write_set_format_zip.argtypes = [c_void_p]
archive_write_set_format_zip.restype = c_int

archive_write_set_format_iso9660 = dll.archive_write_set_format_iso9660
archive_write_set_format_iso9660.argtypes = [c_void_p]
archive_write_set_format_iso9660.restype = c_int

archive_write_add_filter_gzip = dll.archive_write_add_filter_gzip
archive_write_add_filter_gzip.argtypes = [c_void_p]
archive_write_add_filter_gzip.restype = c_int

archive_write_add_filter_compress = dll.archive_write_add_filter_compress
archive_write_add_filter_compress.argtypes = [c_void_p]
archive_write_add_filter_compress.restype = c_int

archive_write_add_filter_none = dll.archive_write_add_filter_none
archive_write_add_filter_none.argtypes = [c_void_p]
archive_write_add_filter_none.restype = c_int

archive_write_set_options = dll.archive_write_set_options
archive_write_set_options.argtypes = [c_void_p, c_char_p]
archive_write_set_options.restype = c_int

archive_write_set_passphrase = dll.archive_write_set_passphrase
archive_write_set_passphrase.argtypes = [c_void_p, c_char_p]
archive_write_set_passphrase.restype = c_int

archive_write_open_filename = dll.archive_write_open_filename
archive_write_open_filename.argtypes = [c_void_p, c_char_p]
archive_write_open_filename.restype = c_int

archive_entry_new = dll.archive_entry_new
archive_entry_new.argtypes = []
archive_entry_new.restype = c_void_p

archive_entry_set_pathname = dll.archive_entry_set_pathname
archive_entry_set_pathname.argtypes = [c_void_p, c_char_p]
archive_entry_set_pathname.restype = None

archive_entry_copy_pathname = dll.archive_entry_copy_pathname
archive_entry_copy_pathname.argtypes = [c_void_p, c_char_p]
archive_entry_copy_pathname.restype = None

archive_entry_set_size = dll.archive_entry_set_size
archive_entry_set_size.argtypes = [c_void_p, c_size_t]
archive_entry_set_size.restype = None

archive_entry_set_mode = dll.archive_entry_set_mode
archive_entry_set_mode.argtypes = [c_void_p, c_ushort]

archive_entry_set_filetype = dll.archive_entry_set_filetype
archive_entry_set_filetype.argtypes = [c_void_p, c_int]
archive_entry_set_filetype.restype = None

archive_entry_set_perm = dll.archive_entry_set_perm
archive_entry_set_perm.argtypes = [c_void_p, c_ushort]
archive_entry_set_perm.restype = None

archive_write_header = dll.archive_write_header
archive_write_header.argtypes = [c_void_p, c_void_p]
archive_write_header.restype = c_int

archive_write_data = dll.archive_write_data
archive_write_data.argtypes = [c_void_p, c_void_p, c_size_t]
archive_write_data.restype = c_int

archive_entry_free = dll.archive_entry_free
archive_entry_free.argtypes = [c_void_p]
archive_entry_free.restype = c_int

archive_write_close = dll.archive_write_close
archive_write_close.argtypes = [c_void_p]
archive_write_close.restype = c_int

archive_write_free = dll.archive_write_free
archive_write_free.argtypes = [c_void_p]
archive_write_free.restype = c_int

