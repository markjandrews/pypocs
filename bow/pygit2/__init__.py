import os
import atexit
import platform
import logging
from ctypes import CDLL

from .api import Api
from .repository import Repo
from .remote import Remote
from .credential import Cred
from .errors import *

GitDirection = Api.GitDirection