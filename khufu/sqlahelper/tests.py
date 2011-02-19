import unittest


class SQLAHelperTests(unittest.TestCase):

    def test_middleware(self):
        from khufu.sqlahelper import SQLAHelper, SQLA_SESSION_KEY

        environ = {}

        class Mock(object):
            def close(self):
                pass
        mock = Mock()

        def get_mock():
            return mock
        helper = SQLAHelper(lambda x, y: None, get_mock)
        helper(environ, None)
        assert environ[SQLA_SESSION_KEY] is mock

    def test_setup_request(self):
        from khufu.sqlahelper import SQLA_SESSION_KEY, setup_request

        class Mock(object):
            class request(object):
                environ = {SQLA_SESSION_KEY: 'foo'}
        setup_request(Mock)
        assert Mock.request.environ[SQLA_SESSION_KEY] is 'foo'

    def test_init_config(self):
        from khufu.sqlahelper import includeme

        class Mock(object):
            called = False

            class registry:
                settings = {}

            def add_subscriber(self, *args):
                self.called = True
        m = Mock()
        includeme(m)
        assert m.called

    def test_get_session_factory(self):
        from khufu.sqlahelper import get_session_factory

        sf = get_session_factory('sqlite://')
        assert callable(sf)

        def mycallable(): None
        self.assertEquals(get_session_factory(mycallable),
                          mycallable)

        self.assertRaises(TypeError, get_session_factory, object())

    def test_with_db(self):
        from khufu.sqlahelper import with_db, SQLAHelper

        class Mock:
            class registry:
                settings = {}

        self.assertRaises(ValueError, with_db, Mock)
        self.assertTrue(isinstance(with_db(object(),
                                           lambda: None), SQLAHelper))


class TraversalTests(unittest.TestCase):

    def test_attrs_traversable_init(self):
        from khufu.sqlahelper.traversalutils import attrs_traversable

        c = attrs_traversable()
        assert c.iterable_attrs == {}

        c = attrs_traversable({})
        assert c.iterable_attrs == {}

    def test_attrs_traversable_call(self):
        from khufu.sqlahelper.traversalutils import (attrs_traversable,
                                                     _AttrIterableWrapper)
        c = attrs_traversable()

        class Mock(object):
            pass
        c(Mock)
        assert issubclass(Mock.wrap, _AttrIterableWrapper)

    def test_AttrIterableWrapper(self):
        from khufu.sqlahelper.traversalutils import _AttrIterableWrapper

        class Mock(object):
            def __init__(self, *args, **kwargs):
                pass

        cls = _AttrIterableWrapper.create_class(Mock.__name__, {'abc': Mock})
        c = cls(None, None)
        self.assertRaises(KeyError, lambda: c['foo'])
        assert isinstance(c['abc'], Mock)

        w = _AttrIterableWrapper('foo', 'bar')
        self.assertRaises(NotImplementedError, lambda: w['abc'])

    def test_TraversalMixin(self):
        from khufu.sqlahelper.traversalutils import TraversalMixin

        m1 = object()
        m2 = object()

        class Mock(object):
            db = m1
        tm = TraversalMixin(parent=Mock)
        assert tm.db is m1

        tm = TraversalMixin(db=m2)
        assert tm.db is m2


from khufu.sqlahelper.traversalutils import DataContainer


class TraversalDataContainerTests(unittest.TestCase):
    class Mock(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.id = 'mock_id'

    class MockSession(set):
        def query(self, *args, **kwargs):
            return self

        def get(self, k):
            return list(self)[0]

    _db = MockSession()

    class MockContainer(DataContainer):
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

    def test_iter(self):
        dc = self.MockContainer()
        self.assertEquals([x.id for x in dc], ['mock_id'])
