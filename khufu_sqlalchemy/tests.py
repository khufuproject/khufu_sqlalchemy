import unittest


class Mock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestSetupFactory(unittest.TestCase):

    def setUp(self):
        self.settings = {}
        self.registry = Mock(settings=self.settings)

    def test_factory_exists(self):
        from khufu_sqlalchemy import _setup_factory, DBSESSION_FACTORY

        def m(): pass
        self.settings[DBSESSION_FACTORY] = m
        self.assertEqual(_setup_factory(self.registry), m)

    def test_engine_exists(self):
        from khufu_sqlalchemy import (
            _setup_factory, DBSESSION_ENGINE, DBSESSION_FACTORY)

        self.settings[DBSESSION_ENGINE] = object()
        _setup_factory(self.registry)
        self.assertTrue(DBSESSION_FACTORY in self.settings)

    def test_sqlalchemy_url(self):
        from khufu_sqlalchemy import (
            _setup_factory, SQLALCHEMY_URL, DBSESSION_FACTORY)
        self.settings[SQLALCHEMY_URL] = 'sqlite:///:memory'
        _setup_factory(self.registry)
        self.assertTrue(DBSESSION_FACTORY in self.settings)


class TestIncludeMe(unittest.TestCase):

    def test_it(self):
        from khufu_sqlalchemy import includeme

        class MockConfig(object):
            def __init__(self):
                self.registry = Mock(settings={})

            def include(self, m):
                pass
        m = MockConfig()

        self.assertRaises(KeyError, includeme, m)


class TestDBSession(unittest.TestCase):

    def test_already_exists(self):
        from khufu_sqlalchemy import dbsession, DBSESSION
        marker = object()
        req = Mock(environ={DBSESSION: marker})
        self.assertEqual(dbsession(req), marker)

    def test_context(self):
        from khufu_sqlalchemy import dbsession
        req = Mock(environ={}, context=Mock())
        req.context.db = marker = object()
        self.assertEqual(dbsession(req), marker)

    def test_object_session(self):
        from khufu_sqlalchemy import _DBSessionFinder
        dbsession = _DBSessionFinder()
        req = Mock(environ={}, context=Mock(),
                   registry=Mock(settings={}))
        self.assertEqual(dbsession(req, False), None)

        marker = object()
        dbsession._object_session = lambda x: marker
        req = Mock(environ={}, context=Mock(),
                  registry=Mock(settings={}))
        self.assertEqual(dbsession(req, False), marker)

    def test_create(self):
        from khufu_sqlalchemy import dbsession, DBSESSION_FACTORY

        self.assertEqual(dbsession(Mock(environ={}), create=False), None)

        marker = object()

        def foo():
            return marker
        m = Mock(environ={},
                 add_finished_callback=lambda x: None,
                 registry=Mock(settings={DBSESSION_FACTORY: foo}))
        self.assertEqual(dbsession(m, create=True), marker)
