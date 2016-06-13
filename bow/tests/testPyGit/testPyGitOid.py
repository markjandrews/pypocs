import os
import stat
import unittest
import shutil

from pygit2.credential import AuthMethods


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestPyGitOid(unittest.TestCase):
    artefacts_dir = 'artefacts'

    @classmethod
    def setUpClass(cls):
        cls.artefacts_dir = os.path.abspath(os.path.join('artefacts', cls.__name__))
        cls.orig_dir = os.getcwd()

        if os.path.exists(cls.artefacts_dir):
            shutil.rmtree(cls.artefacts_dir, onerror=remove_readonly)

        os.makedirs(cls.artefacts_dir)

    def setUp(self):
        pass

    def tearDown(self):
        os.chdir(self.orig_dir)

    def testPyGitOidFromRemote(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo1')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
        remote_heads = remote.ls()
        remote_head = remote_heads['refs/tags/v0.1.0']
        oid = remote_head.oid
        oid_str = oid.fmt()
        self.assertEqual(oid_str, '23f8588dde934e8f33c263c6d8359b2ae095f863')

