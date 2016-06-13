import os
import xml.etree.ElementTree as ET

from . import util
from .errors import ManifestError


class Manifest(object):
    FILENAME = 'manifest.xml'

    def __init__(self, project='', version='', description='', source='', dependencies=None):

        self.project = project
        self.version = version
        self.description = description
        self.source = source

        if dependencies is None:
            dependencies = {}

        assert isinstance(source, (str, type(None))), "Source dependency type (%s) no longer supported" % type(source)
        assert isinstance(dependencies, dict), "Dependency List no longer supported"

        self.dependencies = dependencies

    def to_xml(self):
        root = ET.Element('manifest')
        ET.SubElement(root, 'project').text = self.project if self.project else ''
        ET.SubElement(root, 'version').text = self.version if self.version else ''
        ET.SubElement(root, 'description').text = self.description if self.dep_by_project else ''

        if self.source:
            ET.SubElement(root, 'source').text = self.source if self.source else ''
        else:
            ET.SubElement(root, 'source')

        dependency_xml = ET.SubElement(root, 'dependencies')
        for dependency in self.dependencies.values():
            dependency_xml.append(dependency.to_xml())

        return root

    def dep_by_project(self, project):
        return self.dependencies.get(project.lower(), None)

    def dep_by_source(self):
        return self.dep_by_project(self.source)

    def save(self, workingdir=None, force=False):
        if workingdir is None:
            workingdir = os.getcwd()

        if force is not True:
            manifest_path = self.find_root_path(workingdir=workingdir)
        else:
            manifest_path = os.path.join(workingdir, Manifest.FILENAME)

        with open(manifest_path, 'w', encoding='utf-8') as outf:
            outf.write(util.prettify_xml(self.to_xml()))

    @classmethod
    def from_xml(cls, root_xml: ET.Element):
        from .dependency import Dependency

        project = root_xml.find('.//project').text
        version = root_xml.find('.//version').text
        description = root_xml.find('.//description').text

        source = root_xml.find('.//source').text

        dependencies = {}
        for dependency_xml in root_xml.findall('.//dependencies/*'):
            dependency = Dependency.from_xml(dependency_xml)
            dependencies[dependency.project.lower()] = dependency

        result = Manifest(project=project, version=version, description=description, source=source,
                          dependencies=dependencies)

        return result

    @classmethod
    def find_root_path(cls, workingdir=None):
        if workingdir is None:
            workingdir = os.getcwd()

        workingdir = os.path.abspath(workingdir)
        currentdir = workingdir

        while True:
            if cls.FILENAME.lower() in os.listdir(currentdir):
                break

            newdir = os.path.abspath(os.path.join(currentdir, '..'))
            if newdir == currentdir:
                raise ManifestError('Root manifest path not found')

            currentdir = newdir

        return os.path.join(currentdir, Manifest.FILENAME)

    @classmethod
    def get_root_manifest(cls, workingdir=None):
        if workingdir is None:
            workingdir = os.getcwd()

        workingdir = os.path.abspath(workingdir)

        manifest_path = Manifest.find_root_path(workingdir)
        manifest_xml = ET.parse(manifest_path)
        manifest = Manifest.from_xml(manifest_xml)

        return manifest
