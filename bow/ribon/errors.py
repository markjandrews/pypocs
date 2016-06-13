
class RibonError(BaseException):
    pass


class RibonCmdError(RibonError):
    pass


class ManifestError(RibonError):
    pass


class DependencyError(RibonError):
    pass


class HandlerError(RibonError):
    pass