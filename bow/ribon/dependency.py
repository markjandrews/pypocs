from xml.etree import ElementTree as ET

from .errors import DependencyError


class Dependency(object):
    from .handlers import registered_handlers

    def __init__(self, type, project='', version='', description='', path='', hasmanifest=False, readonly=True,
                 **kwargs):

        self.type = type
        self.project = project
        self.version = version
        self.description = description
        self.path = path
        self.hasmanifest = hasmanifest
        self.readonly = readonly
        self.options = kwargs

        self.handler = self.registered_handlers[type]

    def __getattr__(self, item):
        # Return an optional (specific for dependency type) attribute
        if item in self.options:
            return self.options[item]
        else:
            raise AttributeError

    def to_xml(self):
        attrib = {'project': self.project,
                  'version': self.version,
                  'path': self.path,
                  'hasmanifest': str(self.hasmanifest),
                  'readonly': str(self.readonly)}

        attrib.update({x.lower(): y for x, y in self.options.items()})
        root = ET.Element(self.type, attrib=attrib)

        if self.description is not None:
            ET.SubElement(root, 'description').text = self.description

        return root

    def update(self, **kwargs):

        for key, value in kwargs.items():

            if value is None:
                continue

            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.options[key] = value

    @classmethod
    def from_xml(cls, root_xml: ET.Element):

        attrib = {x.lower(): y for x, y in root_xml.attrib.items()}
        attrib['type'] = root_xml.tag.lower()

        description = root_xml.find('.//description')
        if description is not None:
            attrib['description'] = description.text

        attrib['hasmanifest'] = 'true' in attrib['hasmanifest'].lower()

        result = Dependency(**attrib)
        return result

    @classmethod
    def validate_args(cls, **kwargs):
        from . import registered_handlers

        if 'project' not in kwargs:
            raise DependencyError('Arg: dependency project name not specified')

        if 'type' not in kwargs:
            raise DependencyError('Arg: dependency type not specified')

        if kwargs['type'].lower() not in registered_handlers:
            raise DependencyError('Dependency type (%s) not supported')

        registered_handlers[kwargs['type']].validate_args(**kwargs)
