from pyramid.events import NewRequest
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.engine.base import Engine
from zope.sqlalchemy import ZopeTransactionExtension
from repoze import tm

SQLALCHEMY_URL = 'sqlalchemy.url'
SQLA_SESSION_KEY = 'khufu.pyrasqlalchemy.db_session'


def setup_request(event):
    '''Sets up the 'db' attribute on the request which points
    to an active session.
    '''
    event.request.db = event.request.environ[SQLA_SESSION_KEY]


def includeme(config):
    config.add_subscriber(setup_request, NewRequest)


class SQLAHelper(object):
    '''WSGI middleware for ensuring there is an active session setup and
    handling a transaction via repoze.tm2
    '''

    def __init__(self, application, session_factory):
        self.session_factory = session_factory
        self.application = tm.TM(application)

    def __call__(self, environ, start_response):
        session = environ.get(SQLA_SESSION_KEY, None)
        created = False

        if session is None:
            session = environ[SQLA_SESSION_KEY] = self.session_factory()
            created = True

        try:
            return self.application(environ, start_response)
        finally:
            if created:
                session.close()


def get_session_factory(db):
    '''Returns a session factory based on the given argument.
    :param db: Can be a string (database string), sqlalchemy engine,
               or session factory
    '''
    if isinstance(db, basestring):  # database string
        return get_session_factory(sqlalchemy.create_engine(db))
    elif isinstance(db, Engine):  # engine
        return orm.sessionmaker(bind=db, extension=ZopeTransactionExtension())

    # session factory provided
    if not callable(db):
        raise TypeError('Session factory arg must be either a sqlalchemy url, '
                        'an instance of sqlalchemy Engine, or a session '
                        'factory, not: %s' % str(type(db)))
    return db


def with_db(app, db=None):
    '''Returns a wrapped (with middleware) app.

    :param app: The WSGI application to wrap
    :param db: Can be a string (database string), sqlalchemy engine,
               or sqlalchemy session factory.  If not provided, sqla url
               is looked up in the pyramid registry settings (provided
               by ``app.registry.settings[SQLALCHEMY_URL]``)
    '''

    if db is None:
        db = app.registry.settings.get(SQLALCHEMY_URL, None)

    if db is None:
        raise ValueError('Either the db param or settings[SQLALCHEMY_URL]'
                         ' must be provided')

    return SQLAHelper(app, get_session_factory(db))
