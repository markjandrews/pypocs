import os
import stat
import unittest
import shutil

from testfixtures import LogCapture


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestRibonCmdSet(unittest.TestCase):

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

    def testRibonSetSource(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test1'))
        archive_dir = os.path.join(working_dir, 'archive')

        os.makedirs(archive_dir)

        ribon.main('init %s' % working_dir)
        os.chdir(working_dir)

        with LogCapture() as lc:
            ribon.main('set source nonexistentproject')

        lc.check(
            ('ribon.cmd.dep', 'WARNING',
             'Manifest source (nonexistentproject) does not reference any existing dependency'))

    def testRibonSetSourceExistingDep(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test2'))
        archive_dir = os.path.join(working_dir, 'archive')

        os.makedirs(archive_dir)

        ribon.main('init %s' % working_dir)
        os.chdir(working_dir)

        ribon.main('dep set project2 -t file -o DESTPATH="%s"' % archive_dir)
        ribon.main('set source project2')
