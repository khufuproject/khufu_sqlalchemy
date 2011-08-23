import json
import logging

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import zope.sqlalchemy


logger = logging.getLogger('khufu_sqlalchemy')
khufu_sqlalchemy_logger = logging.getLogger('khufu_sqlalchemy')
if len(khufu_sqlalchemy_logger.handlers) == 0:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
            '%(levelname)s:%(name)s:%(message)s'))
    khufu_sqlalchemy_logger.addHandler(handler)
    khufu_sqlalchemy_logger.propagate = False
    khufu_sqlalchemy_logger.setLevel(logging.INFO)


SQLALCHEMY_URL = 'sqlalchemy.url'
SQLALCHEMY_CONNECT_KWARGS = 'sqlalchemy.connect_kwargs'
DBSESSION = 'khufu.dbsession'
DBSESSION_ENGINE = 'khufu.dbengine'
DBSESSION_ENGINE_KWARGS = 'khufu.dbengine_kwargs'
DBSESSION_FACTORY = 'khufu.dbsession_factory'


def _setup_factory(registry):
    '''Ensure there is a session factory located somewhere in the registry.
    '''

    settings = registry.settings

    if DBSESSION_FACTORY in settings:
        return settings[DBSESSION_FACTORY]

    if DBSESSION_ENGINE in settings:
        engine = settings[DBSESSION_ENGINE]
        factory = sqlalchemy.orm.sessionmaker(
            bind=engine, extension=zope.sqlalchemy.ZopeTransactionExtension(),
            expire_on_commit=False)
        factory = sqlalchemy.orm.scoped_session(factory)
        settings[DBSESSION_FACTORY] = factory
        return factory

    url = settings[SQLALCHEMY_URL]
    kwargs = {}
    if url.startswith('sqlite:'):
        # dealing with a problem with closed connections
        # https://github.com/Pylons/pyramid/issues/174
        import pkg_resources
        pkg = pkg_resources.get_distribution('SQLAlchemy')
        if pkg != None:
            logger.warn('Working around bug with connection pooling and '
                        'sqlite - '
                        'https://github.com/Pylons/pyramid/issues/174')
            from sqlalchemy.pool import NullPool
            kwargs['poolclass'] = NullPool

    additional_kwargs = settings.get(SQLALCHEMY_CONNECT_KWARGS, None)
    if additional_kwargs is not None:
        if isinstance(additional_kwargs, basestring):
            additional_kwargs = json.loads(additional_kwargs)
        for k, v in additional_kwargs.items():
            kwargs[k] = v
    engine = settings[DBSESSION_ENGINE] = \
        sqlalchemy.create_engine(url, **kwargs)
    return _setup_factory(registry)


def includeme(config):
    '''Register components with the pyramid Configurator instance.'''

    config.include('pyramid_tm')
    _setup_factory(config.registry)


class _DBSessionFinder(object):

    _object_session = staticmethod(sqlalchemy.orm.object_session)

    def __init__(self):
        self.count = 0

    def setup_session(self, request):
        environ = request.environ
        if DBSESSION_FACTORY not in request.registry.settings:
            raise ValueError('Please configure khufu_sqlalchemy')

        environ[DBSESSION] = request.registry.settings[DBSESSION_FACTORY]()

        if request.registry.settings.get('DEBUG', False):
            import threading
            thread = threading.current_thread()
            logger.debug('created database session for thread: %s (%i active)'
                         % (thread.name, threading.active_count()))

        self.count += 1
        logger.debug('db session acquired (%i)' % self.count)

        def close(request, dbsession=environ[DBSESSION]):
            try:
                self.count -= 1
                logger.debug('db session closed (%i)' % self.count)
                dbsession.close()
                if hasattr(dbsession, 'remove'):
                    logger.debug('db session removed (%i)' % self.count)
                    dbsession.remove()
            except Exception, ex:
                logger.warning(str(ex))
        request.add_finished_callback(close)

        return environ[DBSESSION]

    def get_session_from_obj(self, request, obj):
        session = getattr(obj, 'db', None)

        if session is None:
            environ = request.environ
            try:
                environ[DBSESSION] = self._object_session(obj)
                session = environ[DBSESSION]
            except sqlalchemy.orm.exc.UnmappedInstanceError:
                pass

        return session

    def __call__(self, request, create=True):
        '''Return the active database session from the object specified.

        The lookup logic is as follows:
          1. If object has ``environ`` attr, check for environ[DBSESSION]
          2. If request has ``db`` attr, use that
          3. If request has a context, trying getting a session from
             that context

        :param request: Normally an instance of ``pyramid.request.Request``
                        but can be any object with either ``db``
                        or ``environ`` and ``registry`` attrs
        :param create: If no db session is active on the reqeust, create one,
                       defaults to True
        '''

        environ = getattr(request, 'environ', {})
        session = environ.get(DBSESSION, None)

        if session is None:
            session = getattr(request, 'db', None)

        if session is None and hasattr(request, 'context'):
            session = self.get_session_from_obj(request, request.context)

        if (session is None or not _is_active(session)) and create:
            if session is not None and not _is_active(session):
                logger.warning('Dropped db session due to being inactive')
            session = self.setup_session(request)

        if session is not None:
            # make sure the new session has the current context
            # ancestry merged in

            obj = getattr(request, 'context', None)
            for x in range(30):
                obj = getattr(obj, '__parent__', None)

                if obj is None:
                    break

                if isinstance(obj, sqlalchemy.ext.declarative.DeclarativeMeta):
                    logger.debug('merged in the context object to active session')
                    session.merge(obj)

        return session


def _is_active(s):
    return getattr(s, 'is_active', True)


dbsession = _DBSessionFinder()
