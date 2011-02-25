from pyramid_traversalwrapper import LocationProxy


class attrs_traversable(object):
    """A decorator that adds a "wrap" attribute to the given class
    in the form of a dict-like class that does item lookup based
    on the attrs given.
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.iterable_attrs = dict(args[0])
            self.iterable_attrs.update(kwargs)
        else:
            self.iterable_attrs = dict(kwargs)

    def __call__(self, cls):
        cls.wrap = _AttrIterableWrapper.create_class(cls.__name__,
                                                     self.iterable_attrs)
        return cls


class _AttrIterableWrapper(LocationProxy):
    """A base class meant to be subclassed and provide a iterable_attrs
    attribute.  This is used as the wrapper class for attrs_traversable.
    """
    iterable_attrs = None

    def __getitem__(self, k):
        if self.iterable_attrs is None:
            raise NotImplementedError(
                'Must define the iterable_attrs attribute')
        if k not in self.iterable_attrs:
            raise KeyError(k)
        callable_ = self.iterable_attrs[k]
        return callable_(k, self)

    @classmethod
    def create_class(cls, name_prefix, iterable_attrs):
        class_name = name_prefix + cls.__name__
        class_bases = (cls,)
        module = cls.__module__ + '.' + cls.__name__.lower()
        class_dict = dict(iterable_attrs=iterable_attrs,
                          __module__=module)
        return type(class_name, class_bases, class_dict)


class TraversalMixin(object):
    """A mixin to provide name, parent, and db attributes.
    """
    __name__ = None
    __parent__ = None
    db = None

    def __init__(self, name=None, parent=None, db=None):
        self.__name__ = name
        self.__parent__ = parent
        self._db = db

    @property
    def db(self):
        if self._db is not None:
            return self._db

        return self.__parent__.db


class DataContainer(TraversalMixin):
    """A container-type object that represents a SQLAlchemy
    data model table.
    """
    model_class = None
    wrap = LocationProxy
    unique_lookup = None
    key_converter = None

    def __iter__(self):
        return (self.wrap(x, self, str(x.id))
                for x in self.db.query(self.model_class))

    def add(self, **kwargs):
        m = self.model_class(**kwargs)
        self.db.add(m)
        return m

    def get_unwrapped_object(self, k):
        if self.unique_lookup is None:
            return self.db.query(self.model_class).get(k)

        # TODO: make this more efficient by turning it into one query
        # instead of using the parent relationship objects and doing
        # a manual filter
        for x in getattr(self.__parent__, self.__name__):
            attr = getattr(x, self.unique_lookup)
            if attr == k:
                return x

        raise KeyError(k)

    def __getitem__(self, k):
        if self.model_class is None:
            raise NotImplementedError('model_class must be specified')

        realk = k
        if self.key_converter is not None:
            realk = self.key_converter(k)
        obj = self.get_unwrapped_object(realk)
        return self.wrap(obj, self, k)
