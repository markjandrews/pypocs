import weakref
from ctypes import *
from enum import IntEnum

from .credential import Cred
from .api import Api
from .errors import check_error, GitReturnCodes, PyGit2ApiError, GitErrorKlass
from .repository import Repo


class GitCredType(IntEnum):
    GIT_CREDTYPE_USERPASS_PLAINTEXT = (1 << 0)
    GIT_CREDTYPE_SSH_KEY = (1 << 1)
    GIT_CREDTYPE_SSH_CUSTOM = (1 << 2)
    GIT_CREDTYPE_DEFAULT = (1 << 3)
    GIT_CREDTYPE_SSH_INTERACTIVE = (1 << 4)
    GIT_CREDTYPE_USERNAME = (1 << 5)
    GIT_CREDTYPE_SSH_MEMORY = (1 << 6)


class ConnectionManager(object):

    def __init__(self, remote, direction=Api.GitDirection.GIT_DIRECTION_FETCH):
        self.remote = remote
        self.direction = direction
        self.alreadyconnected = False

    def __enter__(self):
        self.alreadyconnected = self.remote.connected

        if not self.alreadyconnected:
            self.remote.connect(self.direction)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.alreadyconnected:
            self.remote.disconnect()


class Remote(object):
    GIT_REMOTE_CALLBACKS_VERSION = 1
    GIT_FETCH_OPTIONS_VERSION = 1

    def _finalize(self):
        if self._remote is not None:
            self.disconnect()
            Api.git_remote_free(self._remote)

    def __init__(self, p_raw_remote: c_void_p, repo: Repo):
        self._remote = p_raw_remote
        self._repo = repo
        self._remote_heads = {}
        self.cred = None
        weakref.finalize(self, self._finalize)

    @property
    def connected(self):
        return Api.git_remote_connected(self._remote)

    @property
    def repo(self):
        return self._repo

    @property
    def remote_heads(self):
        if len(self.remote_heads) == 0:
            self.ls()

        return self._remote_heads

    @property
    def name(self):
        return Api.git_remote_name(self._remote).decode('latin-1')

    @property
    def url(self):
        return Api.git_remote_url(self._remote).decode('latin-1')

    def _cred_acquire_cb(self, pp_raw_cred: POINTER(c_void_p), url: bytes, username: bytes, allowed_types: int,
                         payload: c_void_p):

        if self.cred is None:
            return GitReturnCodes.GIT_PASSTHROUGH.value

        if GitCredType.GIT_CREDTYPE_USERNAME & allowed_types == GitCredType.GIT_CREDTYPE_USERNAME:
            if self.cred.username is None:
                self.cred.last_auth_method = len(self.cred.auth_methods)
                return 1

            return Api.git_cred_username_new(pp_raw_cred, self.cred.username.encode('latin-1'))
        else:
            return self.cred.submit(pp_raw_cred=pp_raw_cred, username=username)

    @property
    def fetch_specs(self):
        strarray = Api.git_strarray()
        result = []

        check_error(Api.git_remote_get_fetch_refspecs(byref(strarray), self._remote))

        for i in range(strarray.count):
            fetch_spec = strarray.strings[i].decode('latin-1')
            result.append(fetch_spec)

        Api.git_strarray_free(byref(strarray))

        return result

    @property
    def default_branch(self):
        with ConnectionManager(self, Api.GitDirection.GIT_DIRECTION_FETCH):
            git_buf = Api.git_buf()
            check_error(Api.git_remote_default_branch(byref(git_buf), self._remote))

            branch = git_buf.ptr[:git_buf.size]
            return branch.decode('latin-1')

    def fetch(self):
        with ConnectionManager(self, Api.GitDirection.GIT_DIRECTION_FETCH):

            fetch_options = Api.git_fetch_options()
            check_error(Api.git_fetch_init_options(byref(fetch_options), self.GIT_FETCH_OPTIONS_VERSION))
            fetch_options.callbacks.credentials = Api.git_cred_acquire_cb(self._cred_acquire_cb)
            fetch_options.prune = Api.git_fetch_prune.GIT_FETCH_PRUNE.value
            fetch_options.download_tags = Api.git_remote_autotag_option.GIT_REMOTE_DOWNLOAD_TAGS_AUTO.value

            check_error(Api.git_remote_download(self._remote, None, byref(fetch_options)))

        check_error(
            Api.git_remote_update_tips(self._remote, byref(fetch_options.callbacks), 1, fetch_options.download_tags,
                                       None))

    def connect(self, direction: Api.GitDirection):
        callbacks = Api.git_remote_callbacks()
        check_error(Api.git_remote_init_callbacks(byref(callbacks), self.GIT_REMOTE_CALLBACKS_VERSION))
        callbacks.credentials = Api.git_cred_acquire_cb(self._cred_acquire_cb)

        if self.cred:
            self.cred.last_auth_method = 0

        while True:
            try:
                check_error(Api.git_remote_connect(self._remote, direction.value, byref(callbacks)))
                print('Successfully connected with "%s"' % self.cred.auth_methods[self.cred.last_auth_method - 1])
                break
            except PyGit2ApiError as e:
                if e.klass == GitErrorKlass.GITERR_SSH:
                    if self.cred and self.cred.last_auth_method != len(self.cred.auth_methods):
                        print('Failed to connect with "%s"' % self.cred.auth_methods[self.cred.last_auth_method - 1])
                        continue
                raise

    def disconnect(self):
        if self.connected:
            Api.git_remote_disconnect(self._remote)

    def ls(self):

        with ConnectionManager(self, Api.GitDirection.GIT_DIRECTION_FETCH):
            refs = POINTER(Api.p_git_remote_head)()
            refs_len = c_size_t()
            remote_heads = {}

            check_error(Api.git_remote_ls(byref(refs), byref(refs_len), self._remote))

            for i in range(refs_len.value):
                remote_head = refs[i].contents
                remote_heads[remote_head.name.decode('latin-1')] = remote_head

            return remote_heads
