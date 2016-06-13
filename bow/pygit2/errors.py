from enum import Enum


class PyGit2ApiError(BaseException):

    def __init__(self, err):
        self.klass = GitErrorKlass(err.klass)
        self.message = err.message.decode('latin-1')
        super().__init__('%s: %s' % (self.klass.name, self.message))


class GitErrorKlass(Enum):
    GITERR_NONE = 0
    GITERR_NOMEMORY = 1
    GITERR_OS = 2
    GITERR_INVALID = 3
    GITERR_REFERENCE = 4
    GITERR_ZLIB = 5
    GITERR_REPOSITORY = 6
    GITERR_CONFIG = 7
    GITERR_REGEX = 8
    GITERR_ODB = 9
    GITERR_INDEX = 10
    GITERR_OBJECT = 11
    GITERR_NET = 12
    GITERR_TAG = 13
    GITERR_TREE = 14
    GITERR_INDEXER = 15
    GITERR_SSL = 16
    GITERR_SUBMODULE = 17
    GITERR_THREAD = 18
    GITERR_STASH = 19
    GITERR_CHECKOUT = 20
    GITERR_FETCHHEAD = 21
    GITERR_MERGE = 22
    GITERR_SSH = 23
    GITERR_FILTER = 24
    GITERR_REVERT = 25
    GITERR_CALLBACK = 26
    GITERR_CHERRYPICK = 27
    GITERR_DESCRIBE = 28
    GITERR_REBASE = 29
    GITERR_FILESYSTEM = 30


class GitReturnCodes(Enum):
    GIT_OK = 0
    GIT_ERROR = -1
    GIT_ENOTFOUND = -3
    GIT_EEXISTS = -4
    GIT_EAMBIGUOUS = -5
    GIT_EBUFS = -6
    GIT_EUSER = -7
    GIT_EBAREREPO = -8
    GIT_EUNBORNBRANCH = -9
    GIT_EUNMERGED = -10
    GIT_ENONFASTFORWARD = -11
    GIT_EINVALIDSPEC = -12
    GIT_ECONFLICT = -13
    GIT_ELOCKED = -14
    GIT_EMODIFIED = -15
    GIT_EAUTH = -16
    GIT_ECERTIFICATE = -17
    GIT_EAPPLIED = -18
    GIT_EPEEL = -19
    GIT_EEOF = -20
    GIT_EINVALID = -21
    GIT_EUNCOMMITTED = -22
    GIT_EDIRECTORY = -23
    GIT_PASSTHROUGH = -30
    GIT_ITEROVER = -31

class CredAuthMethodError(BaseException):
    pass

def check_error(value):
    from .import Api

    if value < 0:
        e = Api.giterr_last()
        if e is not False:
            raise PyGit2ApiError(e.contents)

