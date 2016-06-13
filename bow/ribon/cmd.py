import argparse
import os
import logging
from xml.etree import ElementTree as ET

from .errors import DependencyError
from .handlers import registered_handlers

SCRIPT_NAME = 'ribon'


def parse_options(options):
    if options is None:
        options = []

    result = {}
    for option in options:
        key_value = option.split('=', 1)
        key = key_value[0].strip('"\'')
        if len(key_value) > 1:
            value = key_value[1].strip('"\'')
        else:
            value = True

        result[key.lower()] = value

    return result


def init(argv):
    from .manifest import Manifest

    log = logging.getLogger('ribon.cmd.init')

    parser = argparse.ArgumentParser(prog='%s init' % SCRIPT_NAME, description='Initialise a ribon project')
    parser.add_argument('directory', nargs='?', default=None)
    parser.add_argument('-t', '--type', dest='source_type')
    parser.add_argument('-p', '--project')
    parser.add_argument('-v', '--version')
    parser.add_argument('-d', '--description')
    parser.add_argument('-s', '--source', dest='source')
    parser.add_argument('-o', '--options', nargs='*', default=[])
    args, remaining = parser.parse_known_args(argv)

    if args.directory is None:
        args.directory = os.getcwd()

    args.directory = os.path.abspath(args.directory)
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    orig_dir = os.getcwd()
    try:
        os.chdir(args.directory)

        handler = registered_handlers.get(args.source_type)
        if handler is not None:
            handler_options = parse_options(args.options)
            handler.init(project=args.project, version=args.version, **handler_options)
            manifest = handler.fetch_manifest(project=args.project, version=args.version, **handler_options)
        else:
            if os.path.exists(Manifest.FILENAME):
                with open(Manifest.FILENAME, 'r') as inf:
                    manifest = Manifest.from_xml(ET.parse(inf.read()))
            else:
                manifest = Manifest()

            if args.source is not None:
                # ref is a string, so this manifest's source now becomes a reference which we need to check points
                # to a dependency - it may not (yet) so we just print a warning if not
                dependency = manifest.dep_by_project(args.source)
                if not dependency:
                    log.warning('manifest source references dep "%s" that does not exist' % args.source)

                manifest.source = args.source

            manifest.project = args.project if args.project else manifest.project
            manifest.version = args.version if args.version else manifest.version
            manifest.description = args.description if args.description else manifest.description

        if args.project:
            manifest.project = args.project

        if manifest.source is None:
            manifest.source = ''

        manifest.save(force=True)

    finally:
        os.chdir(orig_dir)


def dep_set(**kwargs):
    from .manifest import Manifest
    from .dependency import Dependency

    workingdir = os.getcwd()

    for key, value in kwargs.copy().items():
        if key.lower() == 'options':
            kwargs.update(parse_options(value))
            del kwargs['options']
        elif key.lower() == 'func':
            del kwargs['func']
        elif key.lower() == 'source_type':
            kwargs['type'] = value
            del kwargs['source_type']
        elif key.lower() == 'workingdir':
            workingdir = value
            del kwargs['workingdir']

    Dependency.validate_args(**kwargs)

    manifest = Manifest.get_root_manifest(workingdir=workingdir)
    dependency = manifest.dep_by_project(kwargs['project'])
    if dependency is None:
        dependency = Dependency(kwargs['type'], project=kwargs['project'])
        manifest.dependencies[kwargs['project']] = dependency

    if manifest.source is None:
        manifest.source = ''

    if kwargs['project'].lower() == manifest.source.lower():
        kwargs['hasmanifest'] = True
        kwargs['readonly'] = False

    dependency.update(**kwargs)

    manifest.save(workingdir=workingdir)


def dep_del(project, **kwargs):
    from .manifest import Manifest

    workingdir = kwargs.get('workingdir', os.getcwd())

    manifest = Manifest.get_root_manifest(workingdir=workingdir)
    dependency = manifest.dep_by_project(project)

    if dependency is None or dependency.project not in manifest.dependencies:
        raise DependencyError('Dependency "%s" was not found' % project)

    del manifest.dependencies[dependency.project]

    manifest.save(workingdir=workingdir)


def dep(argv):
    parser = argparse.ArgumentParser(prog='%s dep' % SCRIPT_NAME, description='Update project dependencies')
    subparser = parser.add_subparsers(help='sub-command-help')

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('project', help='Project name')
    parent_parser.add_argument('-w', '--workingdir', default=os.getcwd())

    parser_set = subparser.add_parser('set', parents=[parent_parser])

    parser_del = subparser.add_parser('del', parents=[parent_parser])
    parser_del.set_defaults(func=dep_del)

    manifest_parser = parser_set.add_mutually_exclusive_group(required=False)
    manifest_parser.add_argument('-nm', '--no-manifest', dest='hasmanifest', action='store_false')
    manifest_parser.add_argument('-m', '--manifest', dest='hasmanifest', action='store_true')

    readonly_parser = parser_set.add_mutually_exclusive_group(required=False)
    readonly_parser.add_argument('-nr', '--no-readonly', dest='readonly', action='store_false')
    readonly_parser.add_argument('-r', '--readonly', dest='readonly', action='store_true')

    parser_set.add_argument('-t', '--type', dest='source_type')
    parser_set.add_argument('-v', '--version')
    parser_set.add_argument('-d', '--description')
    parser_set.add_argument('-p', '--path', help='Local relative path to project root')
    parser_set.add_argument('-o', '--options', nargs='*', default=[])
    parser_set.set_defaults(func=dep_set, hasmanifest=None, readonly=None)
    args = parser.parse_args(argv)

    args.func(**vars(args))


def cmd_set(argv):
    from .manifest import Manifest

    log = logging.getLogger('ribon.cmd.dep')

    parser = argparse.ArgumentParser(prog='%s set' % SCRIPT_NAME, description='Update project metadata')
    parser.add_argument('field', choices=['project', 'version', 'description', 'source'])
    parser.add_argument('value', help='value to set field to')
    parser.add_argument('-w', '--workingdir', default=os.getcwd())
    args = parser.parse_args(argv)

    manifest = Manifest.get_root_manifest(workingdir=args.workingdir)
    setattr(manifest, args.field, args.value)

    if args.field.lower() == 'source':
        dependency = manifest.dep_by_source()

        if dependency is None:
            log.warning('Manifest source (%s) does not reference any existing dependency' % args.value)
        else:
            dependency.update(hasmanifest=True, readonly=False)

    if manifest.source is None:
        manifest.source = ''

    manifest.save(workingdir=args.workingdir)
