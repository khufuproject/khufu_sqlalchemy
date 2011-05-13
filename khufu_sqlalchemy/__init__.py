import logging

import sqlalchemy
import sqlalchemy.orm
import zope.sqlalchemy

logger = logging.getLogger('khufu_sqlalchemy')

SQLALCHEMY_URL = 'sqlalchemy.url'
DBSESSION = 'khufu.dbsession'
DBSESSION_ENGINE = 'khufu.dbengine'
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
            bind=engine, extension=zope.sqlalchemy.ZopeTransactionExtension())
        factory = sqlalchemy.orm.scoped_session(factory)
        settings[DBSESSION_FACTORY] = factory
        return factory

    url = settings[SQLALCHEMY_URL]
    kwargs = {}
    if url.startswith('sqlite:'):
        # dealing with a problem with closed connections
        # https://github.com/Pylons/pyramid/issues/174
        import pkg_resources
        pkg = pkg_resources.get_distribution('SQLAlchemy<0.7dev')
        if pkg != None:
            logger.warn('Working around bug with connection pooling and '
                        'sqlite - '
                        'https://github.com/Pylons/pyramid/issues/174')
            from sqlalchemy.pool import NullPool
            kwargs['poolclass'] = NullPool
    engine = settings[DBSESSION_ENGINE] = \
        sqlalchemy.create_engine(url, **kwargs)
    return _setup_factory(registry)


def includeme(config):
    '''Register components with the pyramid Configurator instance.'''

    config.include('pyramid_tm')
    _setup_factory(config.registry)


class _DBSessionFinder(object):

    _object_session = staticmethod(sqlalchemy.orm.object_session)

    def __call__(self, request, create=True):
        '''Return the active database session from the object specified.

        :param request: Normally an instance of ``pyramid.request.Request``
                        but can be any object with ``environ`` and ``registry``
                        attrs
        :param create: If no db session is active on the reqeust, create one,
                       defaults to True
        '''

        environ = request.environ

        if DBSESSION in environ:
            return environ[DBSESSION]

        if hasattr(request, 'context'):
            context = request.context
            if hasattr(context, 'db'):
                return context.db
            try:
                environ[DBSESSION] = self._object_session(context)
                return environ[DBSESSION]
            except sqlalchemy.orm.exc.UnmappedInstanceError:
                pass

        if create:
            environ[DBSESSION] = request.registry.settings[DBSESSION_FACTORY]()

            def close(request, dbsession=environ[DBSESSION]):
                try:
                    dbsession.close()
                except Exception, ex:
                    logger.warning(str(ex))
            request.add_finished_callback(close)
            return environ[DBSESSION]

        return None


dbsession = _DBSessionFinder()
