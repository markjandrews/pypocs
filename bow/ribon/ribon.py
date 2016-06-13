from __future__ import unicode_literals, print_function
import argparse
import os
import shlex
import sys

from . import cmd


def main(argv=sys.argv):

    if isinstance(argv, str):
        argv = [x.strip('"\'') for x in shlex.split(argv, posix='posix' in os.name)]

    parser = argparse.ArgumentParser(description='Package Management all wrapped up in a nice Ribbon')
    subparser = parser.add_subparsers(help='sub-command-help')

    parser_init = subparser.add_parser('init')
    parser_init.set_defaults(func=cmd.init)

    parser_dep = subparser.add_parser('dep')
    parser_dep.set_defaults(func=cmd.dep)

    parser_dep = subparser.add_parser('set')
    parser_dep.set_defaults(func=cmd.cmd_set)

    args, remaining = parser.parse_known_args(argv)
    args.func(remaining)


if __name__ == '__main__':
    exit(main())
