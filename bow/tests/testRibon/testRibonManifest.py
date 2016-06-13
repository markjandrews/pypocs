import os
import stat
import unittest
import shutil


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TestRibonManifest(unittest.TestCase):
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

    def testRibonManifestToXmlWithSourceRef(self):
        from ribon.manifest import Manifest
        from ribon.dependency import Dependency

        working_dir = os.path.join(self.artefacts_dir, 'project1')

        dependency = Dependency(type='file', project='project1dep', version='v1.0', description='This is project1dep',
                                path='.', hasmanifest=True, destpath=os.path.abspath(os.path.join(working_dir)))
        manifest = Manifest(project='project1', version='v1.0', description='This is project1', source="project1dep",
                            dependencies={dependency.project: dependency})

        manifest_xml = manifest.to_xml()
        self.assertEqual('project1', manifest_xml.find('.//project').text)
        self.assertEqual('v1.0', manifest_xml.find('.//version').text)
        self.assertEqual('This is project1', manifest_xml.find('.//description').text)

        dep_xml = manifest_xml.findall('.//dependencies/*')[0]
        self.assertIsNotNone(dep_xml.attrib.get('project', None))
        self.assertEqual(manifest.source, dep_xml.attrib['project'])

    def testRibonManifestToXmlWithSourceInlineFile(self):
        from ribon.manifest import Manifest
        from ribon.dependency import Dependency

        working_dir = os.path.join(self.artefacts_dir, 'project2')

        manifest = Manifest(project='project2', version='v1.0', description='This is project2')
        manifest.source = Dependency(type='file', project='project2dep', version='v1.0',
                                     description='This is project2dep', path='.', hasmanifest=True,
                                     destpath=os.path.abspath(os.path.join(working_dir)))

        self.assertEqual('project2', manifest.project)

        manifest_xml = manifest.to_xml()
        self.assertEqual('project2', manifest_xml.find('.//project').text)
        self.assertEqual('v1.0', manifest_xml.find('.//version').text)
        self.assertEqual('This is project2', manifest_xml.find('.//description').text)

    def testRibonManifestFromXmlWithSourceRef(self):
        from ribon.manifest import Manifest
        from ribon.dependency import Dependency

        working_dir = os.path.join(self.artefacts_dir, 'project3')

        dependency = Dependency(type='file', project='project3dep', version='v1.0', description='This is project3dep',
                                path='.', hasmanifest=True, destpath=os.path.abspath(os.path.join(working_dir)))
        manifest = Manifest(project='project3', version='v1.0', description='This is project3', source="project3dep",
                            dependencies={dependency.project: dependency})

        self.assertEqual('project3', manifest.project)

        manifest_xml = manifest.to_xml()
        new_manifest = Manifest.from_xml(manifest_xml)
        self.assertEqual(new_manifest.source, manifest.source)
