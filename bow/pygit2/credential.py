from __future__ import print_function, unicode_literals
import os
from ctypes import *
from enum import IntEnum
from typing import Sequence

from .api import Api
from .errors import CredAuthMethodError, GitReturnCodes


class AuthMethods(IntEnum):
    agent = 1
    key = 2
    plain = 3


class Cred(object):

    def __init__(self, username: str = None, passphrase: str = None, private_key: str = None, public_key: str = None,
                 methods: Sequence[AuthMethods] = None):

        if methods is None:
            methods = []

        if len(methods) == 0:
            raise CredAuthMethodError('No auth methods provided')

        self.auth_methods = methods
        self.last_auth_method = 0
        self.username = username
        self.passphrase = passphrase
        self.public_key = public_key
        self.private_key = private_key

    def submit(self, pp_raw_cred: POINTER(c_void_p), username: bytes):

        if self.username is not None:
            username = self.username.encode('latin-1')

        if self.last_auth_method == len(self.auth_methods):
            self.last_auth_method = 0
            return GitReturnCodes.GIT_PASSTHROUGH.value

        auth_method = self.auth_methods[self.last_auth_method]
        self.last_auth_method += 1
        print('Attempting "%s" authentication' % auth_method.name)

        if self.passphrase is not None:
            passphrase = self.passphrase.encode('latin-1')
        else:
            passphrase = None

        if auth_method == AuthMethods.agent:
            return Api.git_cred_ssh_key_from_agent(pp_raw_cred, username)

        elif auth_method == AuthMethods.key:
            if self.private_key is None:  # Have to locate public private keys
                ssh_dir = os.path.join(os.path.expanduser('~'), '.ssh')
                if os.path.exists(ssh_dir):
                    keys = ['id_rsa', 'id_dsa', 'identity']
                    for filename in os.listdir(ssh_dir):
                        if filename in keys:
                            self.private_key = os.path.join(ssh_dir, filename)
                            break

            if self.private_key is not None:
                if self.public_key is None:
                    self.public_key = '%s.pub' % self.private_key

            return Api.git_cred_ssh_key_new(pp_raw_cred, username, self.public_key.encode('latin-1'),
                                            self.private_key.encode('latin-1'), passphrase)

        elif auth_method == AuthMethods.plain:
            return Api.git_cred_userpass_plaintext_new(pp_raw_cred, username, self.passphrase.encode('latin-1'))
