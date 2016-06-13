import os
import stat
import unittest
import shutil

from pygit2.credential import AuthMethods


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestPyGitRemote(unittest.TestCase):
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

    def testPyGitRemoteCreate(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo1')

        repo = pygit2.Repo.init(working_dir)

        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        self.assertIsNotNone(remote)

    def testPyGitRemoteLookup(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo2')

        repo = pygit2.Repo.init(working_dir)
        repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')

        remote = repo.remote_lookup('origin')
        self.assertIsNotNone(remote)

    def testPyGitRemoteLookupInvalidRepo(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo3')

        repo = pygit2.Repo.init(working_dir)
        repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')

        with self.assertRaises(pygit2.PyGit2ApiError) as e:
            repo.remote_lookup('invalid')

        self.assertIn('Remote \'invalid\' does not exist.', e.exception.message)

    def testPyGitRemoteConnect(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo4')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
        remote.connect(pygit2.GitDirection.GIT_DIRECTION_FETCH)
        remote.disconnect()

    def testPyGitRemoteConnectNoUsernameInUrl(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo5')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(username='git', methods=[AuthMethods.agent, AuthMethods.key])
        remote.connect(pygit2.GitDirection.GIT_DIRECTION_FETCH)
        remote.disconnect()

    def testPyGitRemoteConnectPriPubKey(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo6')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.key])
        remote.connect(pygit2.GitDirection.GIT_DIRECTION_FETCH)
        remote.disconnect()

    def testPyGitRemoteLs(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo7')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
        remote_heads = remote.ls()
        self.assertTrue(len(remote_heads) > 10)
        self.assertTrue('HEAD' in remote_heads)

    def testPyGitRemoteName(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo8')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])

        self.assertEqual(remote.name, 'origin')

    def testPyGitRemoteUrl(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo9')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])

        self.assertEqual(remote.url, 'git@github.com:markjandrews/libgit2.git')

    def testPyGitRemoteFetchSpecs(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo10')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])

        self.assertEqual(remote.fetch_specs, ['+refs/heads/*:refs/remotes/origin/*'])

    def testPyGitRemoteFetch(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo11')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
        remote.fetch()

    def testPyGitRemoteDefaultBranch(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo12')

        repo = pygit2.Repo.init(working_dir)
        remote = repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remote.cred = pygit2.Cred(methods=[AuthMethods.agent, AuthMethods.key])
        branch = remote.default_branch
        self.assertEqual(branch, 'refs/heads/master')
