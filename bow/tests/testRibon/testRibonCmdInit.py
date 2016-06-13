import os
import stat
import unittest
import shutil
from testfixtures import LogCapture


SCRIPT_DIR = os.path.dirname(__file__)


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestRibonCmdInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.artefacts_dir = os.path.abspath(os.path.join('artefacts', cls.__name__))
        cls.orig_dir = os.getcwd()

        if os.path.exists(cls.artefacts_dir):
            shutil.rmtree(cls.artefacts_dir, onerror=remove_readonly)

        os.makedirs(cls.artefacts_dir)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        os.chdir(self.orig_dir)

    def testRibonInitMainNewManifestWorkingDir(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test1'))
        ribon.main(r'init %s' % working_dir)

    def testRibonInitMainNewManifestNoWorkingDir(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test2'))
        os.makedirs(working_dir)

        orig_dir = os.getcwd()
        try:
            os.chdir(working_dir)
            ribon.main(r'init')
            self.assertTrue(os.path.exists('manifest.xml'))
        finally:
            os.chdir(orig_dir)

    def testRibonInitMainNewManifestWithParams(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test3'))

        os.makedirs(working_dir)
        orig_dir = os.getcwd()

        with LogCapture() as lc:
            try:
                os.chdir(working_dir)
                ribon.main(r'init -p test3 -v v1.0 -d "This is the description for test3" -s test3dep')
            finally:
                os.chdir(orig_dir)

        lc.check(('ribon.cmd.init', 'WARNING', 'manifest source references dep "test3dep" that does not exist'),)

    def testRibonInitMainExistingFileManifest(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test4'))
        archive_dir = os.path.join(working_dir, 'archive')
        os.makedirs(archive_dir)

        os.chdir(working_dir)
        ribon.main(r'init -p test4 -t file -o DESTPATH="%s"' % archive_dir)
        self.assertTrue(False)

    def testRibonInitMainExistingGitManifest(self):
        import ribon
        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test5'))
        os.makedirs(working_dir)
        os.chdir(working_dir)

        ribon.main(r'init -p test5 -t git -o URL="git@github.com:markjandrews/libgit2.git"')
