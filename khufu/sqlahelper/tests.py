import unittest

from khufu import sqlahelper


class SQLAHelperTests(unittest.TestCase):

    def test_middleware(self):
        environ = {}

        class Mock(object):
            def close(self):
                pass
        mock = Mock()

        def get_mock():
            return mock
        helper = sqlahelper.SQLAHelper(lambda x, y: None, get_mock)
        helper(environ, None)
        assert environ[sqlahelper.SQLA_SESSION_KEY] is mock

    def test_setup_request(self):
        class Mock(object):
            class request(object):
                environ = {sqlahelper.SQLA_SESSION_KEY: 'foo'}
        sqlahelper.setup_request(Mock)
        assert Mock.request.environ[sqlahelper.SQLA_SESSION_KEY] is 'foo'

    def test_init_config(self):
        class Mock(object):
            called = False

            class registry:
                settings = {}

            def add_subscriber(self, *args):
                self.called = True
        m = Mock()
        sqlahelper.includeme(m)
        assert m.called

    def test_get_session_factory(self):
        sf = sqlahelper.get_session_factory('sqlite://')
        assert callable(sf)

    def test_with_db(self):
        class Mock:
            class registry:
                settings = {}

        self.assertRaises(ValueError, sqlahelper.with_db, Mock)


from khufu.sqlahelper import traversalutils


class TraversalTests(unittest.TestCase):

    def test_attrs_traversable_init(self):
        c = traversalutils.attrs_traversable()
        assert c.iterable_attrs == {}

        c = traversalutils.attrs_traversable({})
        assert c.iterable_attrs == {}

    def test_attrs_traversable_call(self):
        c = traversalutils.attrs_traversable()

        class Mock(object):
            pass
        c(Mock)
        assert issubclass(Mock.wrap, traversalutils._AttrIterableWrapper)

    def test_AttrIterableWrapper(self):
        class Mock(object):
            def __init__(self, *args, **kwargs):
                pass

        create_class = traversalutils._AttrIterableWrapper.create_class
        cls = create_class(Mock.__name__, {'abc': Mock})
        c = cls(None, None)
        self.assertRaises(KeyError, lambda: c['foo'])
        assert isinstance(c['abc'], Mock)

    def test_TraversalMixin(self):
        m1 = object()
        m2 = object()

        class Mock(object):
            db = m1
        tm = traversalutils.TraversalMixin(parent=Mock)
        assert tm.db is m1

        tm = traversalutils.TraversalMixin(db=m2)
        assert tm.db is m2


class TraversalDataContainerTests(unittest.TestCase):
    class Mock(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class MockSession(set):
        def query(self, *args, **kwargs):
            return self

        def get(self, k):
            return list(self)[0]

    _db = MockSession()

    class MockContainer(traversalutils.DataContainer):
        pass
    MockContainer.model_class = Mock
    MockContainer.db = _db

    def test_add(self):
        dc = self.MockContainer('someattr', self.Mock())
        dc.add(foo=1)

        assert len(self._db) == 1

        assert isinstance(dc.get_unwrapped_object('foo'), self.Mock)
        dc.unique_lookup = 'grr'

        self.Mock.someattr = []
        self.assertRaises(KeyError, lambda: dc.get_unwrapped_object('foo'))

        self.Mock.someattr = [self.Mock(grr='foo')]
        assert isinstance(dc.get_unwrapped_object('foo'), self.Mock)

    def test_getitem(self):
        dc = self.MockContainer()
        assert isinstance(dc['k'], self.Mock)

        class MockContainer(self.MockContainer):
            model_class = None
        dc = MockContainer()
        self.assertRaises(NotImplementedError, lambda: dc['k'])
