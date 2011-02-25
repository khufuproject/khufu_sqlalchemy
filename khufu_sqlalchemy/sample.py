from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPTemporaryRedirect
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.url import resource_url

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

from khufu_sqlalchemy import dbsession
from khufu_sqlalchemy.traversalutils import DataContainer, TraversalMixin


Base = declarative_base()

## database model classes


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)


## traversal model classes

class UserContainer(DataContainer):
    model_class = User
    key_converter = int


class GroupContainer(DataContainer):
    model_class = Group
    key_converter = int


class Root(TraversalMixin, dict):

    def __init__(self, request):
        TraversalMixin.__init__(self, db=dbsession(request))

        self['users'] = UserContainer('users', self, self.db)
        self['groups'] = GroupContainer('groups', self, self.db)


## views

@view_config(context=Root)
def root(request):
    return Response(u'''
  <ul>
    <li><a href="%(root_url)s/users/">Users</a></li>
    <li><a href="%(root_url)s/groups/">Groups</a></li>
  </ul>
''' % {'root_url': request.application_url})


@view_config(context=UserContainer,
             request_method='POST')
@view_config(context=GroupContainer,
             request_method='POST')
def new_item(request):
    db = dbsession(request)
    o = request.context.model_class(name=request.POST['name'])
    db.add(o)
    db.flush()
    o = request.context[str(o.id)]
    url = resource_url(o, request)
    return HTTPTemporaryRedirect(location=url)


@view_config(context=User)
@view_config(context=Group)
def view_item(request):
    return Response(u'''
<a href="../">Back</a>
<dl>
<dt>Type</dt>
<dd>%s</dd>
<dt>Id</dt>
<dd>%s</dd>
<dt>Name</dt>
<dd>%s</dd>
</dl>''' % (str(request.context.__class__.__name__),
            request.context.id, request.context.name))


@view_config(context=GroupContainer)
@view_config(context=UserContainer)
def listing(request):
    s = u'<a href="../">Back</a><ul>'

    for x in request.context:
        s += u'<li><a href="%s">%s</a></li>' % (resource_url(x, request),
                                                x.name)

    s += u'''</ul><form method=post>
New: <input type="text" name="name">
<input type="submit">
</form>'''

    return Response(s)


def app(global_conf, settings):
    '''A factory for creating applications'''

    config = Configurator(settings=settings,
                          root_factory=Root)
    config.scan()
    config.include('khufu_sqlalchemy')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgiapp = app({}, {'sqlalchemy.url': 'sqlite://'})
    engine = wsgiapp.registry.settings['khufu.dbengine']
    Base.metadata.create_all(engine)
    server = make_server('0.0.0.0', 8080, wsgiapp)
    print 'Please see: http://127.0.0.1:8080/'
    server.serve_forever()
