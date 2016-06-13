
class HandlerKlass(type):
    from . import registered_handlers
    _handles = None

    def __init__(cls, name, bases, attr_dict):

        super(HandlerKlass, cls).__init__(name, bases, attr_dict)

        if 'BaseHandler' == name:
            return

        if not issubclass(cls, BaseHandler):
            return

        handles = cls.handles
        if handles is None:
            raise NotImplementedError('Class: "%s" is a dependency handler plugin, yet has no registered type' % cls)

        HandlerKlass.registered_handlers[handles] = cls

    @property
    def handles(cls):
        return cls._handles


class BaseHandler(object, metaclass=HandlerKlass):
    from ..manifest import Manifest

    @classmethod
    def init(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def fetch_manifest(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def validate_args(cls, **kwargs):
        raise NotImplementedError
