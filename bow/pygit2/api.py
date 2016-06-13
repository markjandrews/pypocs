import logging
import os
import platform
from ctypes import *

import atexit
from enum import Enum, IntEnum

SCRIPT_DIR = os.path.dirname(__file__)

logging.basicConfig(level=logging.DEBUG)

PYTHON_ARCH = platform.architecture()[0]
dll_name = 'git2_%s.dll'
if '32bit' in PYTHON_ARCH:
    dll_name %= '32'
else:
    dll_name %= '64'

dll = CDLL(os.path.join(SCRIPT_DIR, 'native', dll_name))
# dll = CDLL(r'C:\Users\Mark\Documents\dev\git\libgit2\build32\Debug\git2.dll')
dll.git_libgit2_init()

atexit.register(dll.git_libgit2_shutdown)


class Api(object):
    class GitDirection(Enum):
        GIT_DIRECTION_FETCH = 0
        GIT_DIRECTION_PUSH = 1

    class git_remote_completion_type(Enum):
        GIT_REMOTE_COMPLETION_DOWNLOAD = 0
        GIT_REMOTE_COMPLETION_INDEXING = 1
        GIT_REMOTE_COMPLETION_ERROR = 2

    class git_fetch_prune(IntEnum):
        GIT_FETCH_PRUNE_UNSPECIFIED = 0
        GIT_FETCH_PRUNE = 1
        GIT_FETCH_NO_PRUNE = 2

    git_fetch_prune_t = c_int

    class git_checkout_notify(IntEnum):
        GIT_CHECKOUT_NOTIFY_NONE = 0,
        GIT_CHECKOUT_NOTIFY_CONFLICT = 1 << 0
        GIT_CHECKOUT_NOTIFY_DIRTY = 1 << 1
        GIT_CHECKOUT_NOTIFY_UPDATED = 1 << 2
        GIT_CHECKOUT_NOTIFY_UNTRACKED = 1 << 3
        GIT_CHECKOUT_NOTIFY_IGNORED = 1 << 4

        GIT_CHECKOUT_NOTIFY_ALL = 0x0FFFF

    git_checkout_notify_t = c_int

    class git_remote_autotag_option(IntEnum):
        GIT_REMOTE_DOWNLOAD_TAGS_UNSPECIFIED = 0
        GIT_REMOTE_DOWNLOAD_TAGS_AUTO = 1
        GIT_REMOTE_DOWNLOAD_TAGS_NONE = 2
        GIT_REMOTE_DOWNLOAD_TAGS_ALL = 3

    git_remote_autotag_option_t = c_int

    class git_checkout_strategy(IntEnum):
        GIT_CHECKOUT_NONE = 0
        GIT_CHECKOUT_SAFE = 1 << 0
        GIT_CHECKOUT_FORCE = 1 << 1
        GIT_CHECKOUT_RECREATE_MISSING = 1 << 2
        GIT_CHECKOUT_ALLOW_CONFLICTS = 1 << 4
        GIT_CHECKOUT_REMOVE_UNTRACKED = 1 << 5
        GIT_CHECKOUT_REMOVE_IGNORED = 1 << 6
        GIT_CHECKOUT_UPDATE_ONLY = 1 << 7
        GIT_CHECKOUT_DONT_UPDATE_INDEX = 1 << 8
        GIT_CHECKOUT_NO_REFRESH = 1 << 9
        GIT_CHECKOUT_SKIP_UNMERGED = 1 << 10
        GIT_CHECKOUT_USE_OURS = 1 << 11
        GIT_CHECKOUT_USE_THEIRS = 1 << 12
        GIT_CHECKOUT_DISABLE_PATHSPEC_MATCH = 1 << 13
        GIT_CHECKOUT_SKIP_LOCKED_DIRECTORIES = 1 << 18
        GIT_CHECKOUT_DONT_OVERWRITE_IGNORED = 1 << 19
        GIT_CHECKOUT_CONFLICT_STYLE_MERGE = 1 << 20
        GIT_CHECKOUT_CONFLICT_STYLE_DIFF3 = 1 << 21
        GIT_CHECKOUT_DONT_REMOVE_EXISTING = 1 << 22
        GIT_CHECKOUT_DONT_WRITE_INDEX = 1 << 23
        GIT_CHECKOUT_UPDATE_SUBMODULES = 1 << 16
        GIT_CHECKOUT_UPDATE_SUBMODULES_IF_CHANGED = 1 << 17

    git_checkout_strategy_t = c_int

    class git_error(Structure):
        pass

    class git_remote_callbacks(Structure):
        pass

    class git_oid(Structure):
        def fmt(self):
            out = (c_char * 40)()
            Api.git_oid_fmt(out, self)
            return out.value.decode('latin-1')

        @classmethod
        def fromstr(cls, instr):
            from . import check_error

            out = Api.git_oid()
            check_error(Api.git_oid_fromstr(byref(out), instr))
            return out

    class git_push_update(Structure):
        pass

    class git_remote_head(Structure):
        pass

    class git_strarray(Structure):
        pass

    class git_fetch_options(Structure):
        pass

    class git_buf(Structure):
        pass

    class git_checkout_options(Structure):
        pass

    class git_diff_file(Structure):
        pass

    class git_checkout_perfdata(Structure):
        pass

    p_git_repository = c_void_p
    p_git_cred = c_void_p
    p_git_transport = c_void_p
    p_git_remote = c_void_p
    p_git_remote_head = POINTER(git_remote_head)
    p_git_oid = POINTER(git_oid)
    p_git_object = c_void_p
    git_off_t = c_int64
    p_git_tree = c_void_p
    p_git_index = c_void_p

    git_repository_init = dll.git_repository_init
    git_repository_init.argtypes = [POINTER(p_git_repository), c_char_p, c_uint]
    git_repository_init.restype = c_int

    git_repository_open = dll.git_repository_open
    git_repository_open.argtypes = [POINTER(p_git_repository), c_char_p]
    git_repository_open.restype = c_int

    git_repository_free = dll.git_repository_free
    git_repository_free.argtypes = [p_git_repository]
    git_repository_free.restype = None

    git_remote_create = dll.git_remote_create
    git_remote_create.argtypes = [POINTER(p_git_remote), p_git_repository, c_char_p, c_char_p]
    git_remote_create.restype = c_int

    git_remote_create_with_fetchspec = dll.git_remote_create_with_fetchspec
    git_remote_create_with_fetchspec.argtypes = [POINTER(p_git_remote), p_git_repository, c_char_p, c_char_p, c_char_p]
    git_remote_create_with_fetchspec.restype = c_int

    git_remote_lookup = dll.git_remote_lookup
    git_remote_lookup.argtypes = [POINTER(p_git_remote), c_void_p, c_char_p]
    git_remote_lookup.restype = c_int

    git_remote_init_callbacks = dll.git_remote_init_callbacks
    git_remote_init_callbacks.argtypes = [POINTER(git_remote_callbacks), c_int]
    git_remote_init_callbacks.restype = c_int

    git_remote_connect = dll.git_remote_connect
    git_remote_connect.argtypes = [p_git_remote, c_int, POINTER(git_remote_callbacks)]
    git_remote_connect.restype = c_int

    git_remote_connected = dll.git_remote_connected
    git_remote_connected.argtypes = [p_git_remote]
    git_remote_connected.restype = c_bool

    git_remote_disconnect = dll.git_remote_disconnect
    git_remote_disconnect.argtypes = [p_git_remote]
    git_remote_disconnect.restype = None

    git_remote_ls = dll.git_remote_ls
    git_remote_ls.argtypes = [POINTER(POINTER(p_git_remote_head)), POINTER(c_size_t), p_git_remote]
    git_remote_ls.restype = c_int

    git_remote_default_branch = dll.git_remote_default_branch
    git_remote_default_branch.argtypes = [POINTER(git_buf), p_git_remote]
    git_remote_default_branch.restype = c_int

    git_remote_list = dll.git_remote_list
    git_remote_list.argtypes = [POINTER(git_strarray), p_git_repository]
    git_remote_list.restype = c_int

    git_remote_name = dll.git_remote_name
    git_remote_name.argtypes = [p_git_remote]
    git_remote_name.restype = c_char_p

    git_remote_url = dll.git_remote_url
    git_remote_url.argtypes = [p_git_remote]
    git_remote_url.restype = c_char_p

    git_remote_free = dll.git_remote_free
    git_remote_free.argtypes = [c_void_p]
    git_remote_free.restype = None

    git_remote_get_fetch_refspecs = dll.git_remote_get_fetch_refspecs
    git_remote_get_fetch_refspecs.argtypes = [POINTER(git_strarray), p_git_remote]
    git_remote_get_fetch_refspecs.restype = c_int

    git_cred_ssh_key_from_agent = dll.git_cred_ssh_key_from_agent
    git_cred_ssh_key_from_agent.argtypes = [POINTER(p_git_cred), c_char_p]
    git_cred_ssh_key_from_agent.restype = c_int

    git_cred_ssh_key_new = dll.git_cred_ssh_key_new
    git_cred_ssh_key_new.argtypes = [POINTER(p_git_cred), c_char_p, c_char_p, c_char_p, c_char_p]
    git_cred_ssh_key_new.restype = c_int

    git_cred_userpass_plaintext_new = dll.git_cred_userpass_plaintext_new
    git_cred_userpass_plaintext_new.argtypes = [POINTER(p_git_cred), c_char_p, c_char_p]
    git_cred_userpass_plaintext_new.restype = c_int

    git_cred_username_new = dll.git_cred_username_new
    git_cred_username_new.argtypes = [POINTER(p_git_cred), c_char_p]
    git_cred_username_new.restype = c_int

    giterr_last = dll.giterr_last
    giterr_last.argtypes = []
    giterr_last.restype = POINTER(git_error)

    git_oid_fmt = dll.git_oid_fmt
    git_oid_fmt.argtypes = [c_char_p, p_git_oid]
    git_oid_fmt.restype = None

    git_oid_fromstr = dll.git_oid_fromstr
    git_oid_fromstr.argtypes = [p_git_oid, c_char_p]
    git_oid_fromstr.restype = c_int

    git_strarray_free = dll.git_strarray_free
    git_strarray_free.argtypes = [POINTER(git_strarray)]
    git_strarray_free.restype = None

    git_fetch_init_options = dll.git_fetch_init_options
    git_fetch_init_options.argtypes = [POINTER(git_fetch_options), c_uint]
    git_fetch_init_options.restype = c_int

    git_remote_download = dll.git_remote_download
    git_remote_download.argtypes = [p_git_remote, POINTER(git_strarray), POINTER(git_fetch_options)]
    git_remote_download.restype = c_int

    git_remote_update_tips = dll.git_remote_update_tips
    git_remote_update_tips.argtypes = [p_git_remote, POINTER(git_remote_callbacks), c_int, git_remote_autotag_option_t,
                                       c_char_p]
    git_remote_update_tips.restype = c_int

    git_buf_free = dll.git_buf_free
    git_buf_free.argtypes = [POINTER(git_buf)]
    git_buf_free.restype = None

    git_checkout_init_options = dll.git_checkout_init_options
    git_checkout_init_options.argtypes = [POINTER(git_checkout_options), c_uint32]
    git_checkout_init_options.restype = c_int

    git_checkout_tree = dll.git_checkout_tree
    git_checkout_tree.argtypes = [p_git_repository, p_git_object, POINTER(git_checkout_options)]
    git_checkout_tree.restype = c_int

    git_revparse_single = dll.git_revparse_single
    git_revparse_single.argtypes = [POINTER(p_git_object), p_git_repository, c_char_p]
    git_revparse_single.restype = c_int

    git_transport_message_cb = CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
    git_cred_acquire_cb = CFUNCTYPE(c_int, POINTER(p_git_cred), c_char_p, c_char_p, c_uint, c_void_p)
    git_transport_certificate_check_cb = CFUNCTYPE(c_int, c_void_p, c_int, c_char_p, c_void_p)
    git_transfer_progress_cb = CFUNCTYPE(c_int, c_void_p, c_void_p)
    git_packbuilder_progress = CFUNCTYPE(c_int, c_int, c_uint, c_uint, c_void_p)
    git_push_transfer_progress = CFUNCTYPE(c_int, c_uint, c_uint, c_int, c_void_p)
    git_push_negotiation = CFUNCTYPE(c_int, POINTER(POINTER(git_push_update)), c_int, c_void_p)
    git_transport_cb = CFUNCTYPE(c_int, POINTER(p_git_transport), c_void_p, c_void_p)
    git_checkout_notify_cb = CFUNCTYPE(c_int, git_checkout_notify_t, c_char_p, POINTER(git_diff_file),
                                       POINTER(git_diff_file), POINTER(git_diff_file), c_void_p)
    git_checkout_progress_cb = CFUNCTYPE(None, c_char_p, c_size_t, c_size_t, c_void_p)
    git_checkout_perfdata_cb = CFUNCTYPE(None, POINTER(git_checkout_perfdata), c_void_p)

    git_error._fields_ = [('message', c_char_p),
                          ('klass', c_int)]

    git_remote_callbacks._fields_ = [('version', c_uint),
                                     ('sideband_progress', git_transport_message_cb),
                                     ('completion', CFUNCTYPE(c_int, c_int, c_void_p)),
                                     ('credentials', git_cred_acquire_cb),
                                     ('certificate_check', git_transport_certificate_check_cb),
                                     ('transfer_progress', git_transfer_progress_cb),
                                     ('update_tips',
                                      CFUNCTYPE(c_int, c_char_p, POINTER(git_oid), POINTER(git_oid), c_void_p)),
                                     ('pack_progress', git_packbuilder_progress),
                                     ('push_transfer_progress', git_push_transfer_progress),
                                     ('push_update_reference', CFUNCTYPE(c_int, c_char_p, c_char_p, c_void_p)),
                                     ('push_negotiation', git_push_negotiation),
                                     ('transport', git_transport_cb),
                                     ('payload', c_void_p)]

    git_oid._fields_ = [('id', c_char * 20)]

    git_push_update._fields_ = [('src_refname', c_char_p),
                                ('dst_refname', c_char_p),
                                ('src', git_oid),
                                ('dst', git_oid)]

    git_remote_head._fields_ = [('local', c_int),
                                ('oid', git_oid),
                                ('loid', git_oid),
                                ('name', c_char_p),
                                ('symref_target', c_char_p)]

    git_strarray._fields_ = [('strings', POINTER(c_char_p)),
                             ('count', c_size_t)]

    git_fetch_options._fields_ = [('version', c_int),
                                  ('callbacks', git_remote_callbacks),
                                  ('prune', git_fetch_prune_t),
                                  ('update_fetchhead', c_int),
                                  ('download_tags', git_remote_autotag_option_t)]

    git_buf._fields_ = [('ptr', c_char_p),
                        ('asize', c_size_t),
                        ('size', c_size_t)]

    git_checkout_options._fields_ = [('version', c_uint),
                                     ('checkout_strategy', c_uint),
                                     ('disable_filters', c_int),
                                     ('dir_mode', c_uint),
                                     ('file_mode', c_uint),
                                     ('file_open_flags', c_int),
                                     ('notify_flags', c_uint),
                                     ('notify_cb', git_checkout_notify_cb),
                                     ('notify_payload', c_void_p),
                                     ('progress_cb', git_checkout_progress_cb),
                                     ('progress_payload', c_void_p),
                                     ('paths', git_strarray),
                                     ('base_line', p_git_tree),
                                     ('base_line_index', p_git_index),
                                     ('target_directory', c_char_p),
                                     ('ancestor_label', c_char_p),
                                     ('out_label', c_char_p),
                                     ('their_label', c_char_p),
                                     ('perfdata_cb', git_checkout_perfdata_cb),
                                     ('perfdata_payload', c_void_p)]

    git_diff_file._fields_ = [('id', git_oid),
                              ('path', c_char_p),
                              ('size', git_off_t),
                              ('flags', c_uint32),
                              ('mode', c_uint16)]

    git_checkout_perfdata._fields_ = [('mkdir_calls', c_size_t),
                                      ('stat_calls', c_size_t),
                                      ('chmod_calls', c_size_t)]
