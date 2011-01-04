from pyramid.events import subscriber, NewRequest
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.engine.base import Engine
from zope.sqlalchemy import ZopeTransactionExtension
from repoze import tm


SQLA_SESSION_KEY = 'khufu.sqlalchemy.session'


def setup_request(event):
    '''Sets up the 'db' attribute on the request which points
    to an active session.
    '''
    event.request.db = event.request.environ[SQLA_SESSION_KEY]

def init_config(config):
    config.add_subscriber(setup_request, NewRequest)

class _SQLAHelper(object):
    '''WSGI middleware for ensuring there is an active session setup.
    '''

    def __init__(self, app, session_factory):
        self.app = app
        self.session_factory = session_factory

    def __call__(self, environ, start_response):
        if environ.get(SQLA_SESSION_KEY, None) is None:
            environ[SQLA_SESSION_KEY] = self.session_factory()
        return self.app(environ, start_response)

def get_session_factory(db):
    '''Returns a session factory based on the given argument.
    :param db: Can be a string (database string), sqlalchemy engine, or session factory
    '''
    if isinstance(db, basestring):  # database string
        return get_session_factory(sqlalchemy.create_engine(db))
    elif isinstance(db, Engine):  # engine
        return get_session_factory(orm.sessionmaker(bind=db, extension=ZopeTransactionExtension()))

    # session factory provided
    return db

def with_db(app, db):
    '''Returns a wrapped (with middleware) app that takes a db argument.
    :param db: Can be a string (database string), sqlalchemy engine, or session factory
    '''
    return _SQLAHelper(app, get_session_factory(db))
