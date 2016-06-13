import weakref
from ctypes import *
from functools import reduce
from operator import ior

from pygit2.object import GitObject
from .credential import Cred
from .errors import check_error
from .api import Api


class Repo(object):
    GIT_CHECKOUT_OPTIONS_VERSION = 1

    def _finalize(self):
        if self._repo is not None:
            Api.git_repository_free(self._repo)

    def __init__(self, repoptr: c_void_p):
        self._repo = repoptr
        weakref.finalize(self, self._finalize)

    def remote_create(self, name: str, url: str, fetch_spec: str = None):
        from .remote import Remote

        remoteptr = c_void_p()
        repoptr = self._repo

        if fetch_spec:
            check_error(Api.git_remote_create_with_fetchspec(byref(remoteptr), repoptr, name.encode('latin-1'),
                                                             url.encode('latin-1'), fetch_spec.encode('latin-1')))
        else:
            check_error(Api.git_remote_create(byref(remoteptr), repoptr, name.encode('latin-1'), url.encode('latin-1')))

        return Remote(p_raw_remote=remoteptr, repo=self)

    def remote_lookup(self, name):
        from .remote import Remote

        remoteptr = c_void_p()
        repoptr = self._repo

        check_error(Api.git_remote_lookup(byref(remoteptr), repoptr, name.encode('latin-1')))

        return Remote(p_raw_remote=remoteptr, repo=self)

    @property
    def remotes(self):
        strarray = Api.git_strarray()
        result = []

        check_error(Api.git_remote_list(byref(strarray), self._repo))

        for i in range(strarray.count):
            name = strarray.strings[i].decode('latin-1')
            result.append(self.remote_lookup(name))

        Api.git_strarray_free(byref(strarray))

        return result

    def checkout_tree(self, treeish, paths=None, checkout_strategy=Api.git_checkout_strategy.GIT_CHECKOUT_NONE):

        options = Api.git_checkout_options()
        check_error(Api.git_checkout_init_options(byref(options), self.GIT_CHECKOUT_OPTIONS_VERSION))

        if not isinstance(checkout_strategy, list):
            checkout_strategy = [checkout_strategy]

        checkout_strategy = reduce(ior, [x.value for x in checkout_strategy])
        options.checkout_strategy = checkout_strategy

        if paths is None:
            paths = []

        if len(paths) > 0:
            cstr_paths = (c_char_p * len(paths))()
            cstr_paths[:] = [x.encode('latin-1') for x in paths]

            strarr = Api.git_strarray()
            strarr.count = len(paths)
            strarr.strings = cstr_paths
            options.paths = strarr

        check_error(Api.git_checkout_tree(self._repo, treeish._object, byref(options)))

    def revparse_single(self, rev):

        treeish = Api.p_git_object()
        rev = rev.encode('latin-1')

        check_error(Api.git_revparse_single(byref(treeish), self._repo, rev))
        return GitObject(treeish)

    @classmethod
    def init(cls, path: str, isbare: bool = False):
        if isbare is True:
            isbare = 1
        else:
            isbare = 0

        repoptr = Api.p_git_repository()

        check_error(Api.git_repository_init(byref(repoptr), path.encode('latin-1'), isbare))

        return Repo(repoptr=repoptr)

    @classmethod
    def open(cls, path: str = None):

        if path is None:
            path = ''

        repoptr = c_void_p()
        check_error(Api.git_repository_open(byref(repoptr), path.encode('latin-1')))

        return Repo(repoptr=repoptr)
