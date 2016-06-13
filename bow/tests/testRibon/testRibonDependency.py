import os
import stat
import unittest
import shutil


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestRibonDependency(unittest.TestCase):
    artefacts_dir = 'artefacts'

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

    def testRibonFileDependencyToXml(self):
        from ribon.dependency import Dependency

        working_dir = os.path.join(self.artefacts_dir, 'project1')

        dependency = Dependency(type='file', project='project2', version='v1.0', hasmanifest=True,
                                description='This is project2 dependency', path='.', dest_path=os.path.join(working_dir))

        dependency_xml = dependency.to_xml()
        self.assertEqual('project2', dependency_xml.attrib['project'])
        self.assertEqual('v1.0', dependency_xml.attrib['version'])
        self.assertEqual('This is project2 dependency', dependency_xml.find('.//description').text)

    def testRibonFileDependencyFromXml(self):
        from ribon.dependency import Dependency

        working_dir = os.path.join(self.artefacts_dir, 'project1')

        dependency = Dependency(type='file', project='project2', version='v1.0', hasmanifest=True,
                                description='This is project 2 dependency', path='.',
                                dest_path=os.path.join(working_dir))

        dependency_xml = dependency.to_xml()
        new_dependency = Dependency.from_xml(dependency_xml)

        self.assertEqual(dependency.type, new_dependency.type)

