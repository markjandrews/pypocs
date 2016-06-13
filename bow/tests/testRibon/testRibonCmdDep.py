import os
import stat
import unittest
import shutil


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestRibonCmdDep(unittest.TestCase):

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

    def testRibonDepAdd(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test1'))
        archive_dir = os.path.join(working_dir, 'archive')

        os.makedirs(archive_dir)

        ribon.main('init %s' % working_dir)
        os.chdir(working_dir)
        ribon.main(
            'dep set project1 -t file -v v1.0 -d "this is the description" -m -p "." -o DESTPATH=%s' % archive_dir)

    def testRibonDepDel(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test2'))
        archive_dir = os.path.join(working_dir, 'archive')

        ribon.main('init %s' % working_dir)
        os.chdir(working_dir)
        ribon.main(
            'dep set project1 -t file -v v1.0 -d "this is the description" -m -p "." -o DESTPATH=%s' % archive_dir)

        ribon.main('dep del project1')

    def testRibonDepUpdate(self):
        import ribon

        working_dir = os.path.abspath(os.path.join(self.artefacts_dir, 'test3'))
        archive_dir = os.path.join(working_dir, 'archive')

        os.makedirs(archive_dir)

        ribon.main('init %s' % working_dir)
        os.chdir(working_dir)
        ribon.main(
            'dep set project1 -t file -v v1.0 -d "this is the description" -m -p "." -o DESTPATH=%s' % archive_dir)

        ribon.main(
            'dep set project1 -t git -v v1.1 -d "this is another description" -m -p "." -o URL=http://www.google.com')
