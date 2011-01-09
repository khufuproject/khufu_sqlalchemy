import unittest

from khufu import sqlahelper


class SQLAHelperTests(unittest.TestCase):

    def test_middleware(self):
        environ = {}
        class Mock(object):
            def close(self): pass
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
            def add_subscriber(self, *args):
                self.called = True
        m = Mock()
        sqlahelper.init_config(m)
        assert m.called

    def test_get_session_factory(self):
        sf = sqlahelper.get_session_factory('sqlite://')
        assert callable(sf)

    def test_with_db(self):
        s = sqlahelper.with_db(None, lambda: None)
        assert isinstance(s, sqlahelper.SQLAHelper)
