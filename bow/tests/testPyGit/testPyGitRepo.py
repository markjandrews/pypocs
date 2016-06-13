import os
import stat
import unittest
import shutil


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestPyGitRepo(unittest.TestCase):
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


    def testPyGitRepoInitWithWorkingDir(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo1')
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

        self.assertFalse(os.path.exists(working_dir))
        pygit2.Repo.init(working_dir)
        self.assertTrue(os.path.exists(os.path.join(working_dir, '.git')))

    def testPyGitRepoOpenWithWorkingDir(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo2')
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)
        pygit2.Repo.init(working_dir)

        repo = pygit2.Repo.open(working_dir)
        self.assertIsNotNone(repo)

    def testPyGitRepoOpenWithoutWorkingDir(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo3')
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

        pygit2.Repo.init(working_dir)

        os.chdir(working_dir)
        repo = pygit2.Repo.open()

        self.assertIsNotNone(repo)

    def testPyGitRepoRemotes(self):
        import pygit2

        working_dir = os.path.join(self.artefacts_dir, 'repo3')
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

        pygit2.Repo.init(working_dir)

        os.chdir(working_dir)
        repo = pygit2.Repo.open()
        repo.remote_create('origin', 'git@github.com:markjandrews/libgit2.git')
        remotes = repo.remotes

