import os

from pygit2 import Api
from pygit2.remote import ConnectionManager
from pygit2.repository import Repo
from pygit2.credential import Cred, AuthMethods

from ..errors import HandlerError
from ..manifest import Manifest

from .base_handler import BaseHandler


class GitHandler(BaseHandler):
    _handles = 'git'

    if 'posix' in os.name:
        auth_methods = [AuthMethods.key, AuthMethods.agent]
    elif 'nt' in os.name:
        auth_methods = [AuthMethods.agent, AuthMethods.key]
    else:
        raise NotImplementedError('Unsupported os "%s"' % os.name)

    @classmethod
    def init(cls, project=None, version=None, url=None, branch=None, workingdir=None, **kwargs):

        if not workingdir:
            workingdir = os.getcwd()

        if not os.path.exists(workingdir):
            os.makedirs(workingdir)

        repo = Repo.init(workingdir)
        remote = repo.remote_create(project, url)
        remote.cred = Cred(username='git', methods=cls.auth_methods)
        remote.fetch()

    @classmethod
    def fetch_manifest(cls, project=None, version=None, branch=None, workingdir=None, **kwargs):

        if not workingdir:
            workingdir = os.getcwd()

        orig_dir = os.getcwd()
        try:
            os.chdir(workingdir)

            repo = Repo.open()
            remote = repo.remote_lookup(project)
            remote.cred = Cred(username='git', methods=cls.auth_methods)

            if version:
                fetch_version = version
            elif branch:
                fetch_version = 'project/branch'
            else:
                with ConnectionManager(remote):
                    branches = remote.ls()
                    default_branch = branches[remote.default_branch]
                    fetch_version = default_branch.oid.fmt()

            treeish = repo.revparse_single(fetch_version)
            repo.checkout_tree(treeish, ['src/attr.c'],
                               checkout_strategy=[Api.git_checkout_strategy.GIT_CHECKOUT_FORCE,
                                                  Api.git_checkout_strategy.GIT_CHECKOUT_DISABLE_PATHSPEC_MATCH])

        finally:
            os.chdir(orig_dir)

        manifest = Manifest()
        return manifest

    @classmethod
    def validate_args(cls, **kwargs):
        if 'url' not in kwargs:
            raise HandlerError('GIT Handler Arg: git dependency url not specified')


class FileHandler(BaseHandler):
    _handles = 'file'

    @classmethod
    def init(cls, project=None, version=None, path=None, workingdir=None, **kwargs):
        if not workingdir:
            workingdir = os.getcwd()

        if not os.path.exists(workingdir):
            os.makedirs(workingdir)

    @classmethod
    def fetch_manifest(cls, project=None, version=None, path=None, **kwargs):
        manifest = Manifest()

        return manifest

    @classmethod
    def validate_args(cls, **kwargs):
        if 'destpath' not in kwargs:
            raise HandlerError('FILE Handler Arg: dependency file destination path not specified')
