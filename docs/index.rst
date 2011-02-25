================
khufu_sqlalchemy
================

Overview
========

khufu_sqlalchemy is an opinionated way of managing :term:`SQLAlchemy` based
connections with :term:`Pyramid`.

Requirements
============

  * Python >= 2.5 (not tested with Python 3.x series)

Setup
=====

Before including :term:`khufu_sqlalchemy` config support it is important
to have one of the three prerequisites fulfilled within the
``config.registry.settings`` dict:

  1. Provide ``sqlalchemy.url``.  In this scenario, :term:`khufu_sqlalchemy`
     will build up the sqlalchemy :term:`engine` and :term:`session factory`
     on config inclusion.  An example:

     .. code-block:: python
      :linenos:

      from pyramid.config import Configurator

      config = Configurator(settings={'sqlalchemy.url': 'sqlite:///:memory'})
      config.include('khufu_sqlalchemy')

  2. Provide ``khufu.dbengine``.  In this scenario, :term:`khufu_sqlalchemy`
     will build up the sqlalchemy :term:`session factory` on config inclusion.

     .. code-block:: python
      :linenos:

      from pyramid.config import Configurator
      from sqlalchemy import create_engine

      engine = create_engine('sqlite:///:memory')
      config = Configurator(settings={'khufu.dbengine': engine})
      config.include('khufu_sqlalchemy')

  3. The last option is to provide ``khufu.dbsession_factory``.  In this scenario,
     nothing else needs to be looked up by :term:`khufu_sqlalchemy`. 

     .. code-block:: python
      :linenos:

      from pyramid.config import Configurator
      from sqlalchemy import create_engine
      from sqlalchemy.orm import scoped_session, sessionmaker

      engine = create_engine('sqlite:///:memory')
      Session = scoped_session(sessionmaker(bind=engine))
      config = Configurator(settings={'khufu.dbsession_factory': Session})
      config.include('khufu_sqlalchemy')

Usage
=====

The standard way to lookup the active database session is as follows:

.. code-block:: python
 :linenos:

 from pyramid.view import view_config
 from pyramid_sqlalchemy import dbsession

 @view_config(context=SomeContainer)
 def users_view(request):
     db = dbsession(request)
     return {'items': db.query(SomeDBModel).all()}

NOTE #1: The ``db`` object is a simple instance of a :term:`SQLAlchemy`
database session.  You should never commit this directly or worry
about closing it.  The :term:`transaction` package takes care of this.

NOTE #2: The :term:`SQLAlchemy` database session is created lazily
upon first dbsession() use.  Multiple calls to dbsession(request)
will each return the same session as long as the request is the same.

Transaction Handling
====================

If your application requires control over the transaction handling,
please use the :term:`transaction` and :term:`pyramid_tm` api's.

Credits
=======

  * Developed and maintained by Rocky Burt <rocky AT serverzen DOT com>

More Information
================

.. toctree::
 :maxdepth: 1

 api.rst
 glossary.rst

Indices and tables
==================

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
