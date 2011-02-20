====================
Khufu-PyraSQLAlchemy
====================

Overview
========

Khufu-PyraSQLAlchemy is meant to reduce the plumbing required to configure a
:term:`SQLAlchemy` based database connection with a :term:`Pyramid` based web app.


Requirements
============

  * Python >= 2.6 (not tested with Python 3.x series)

Requirements Satisfied by Installing
------------------------------------

  * :term:`Pyramid`
  * :term:`SQLAlchemy`
  * :term:`zope.sqlalchemy`
  * :term:`repoze.tm2`
  * :term:`transaction`
  * :term:`pyramid_traversalwrapper`

*NOTE 1: The SQLAHelper middleware includes the repoze.tm2 middleware*
*NOTE 2: The SQLAHelper middleware requires that the app being wrapped was generated by Pyramid*

Usage
=====

Database Configuration
----------------------

To use SQLAHelper database configuration there are two steps:

  1. Hook up the configuration via ``configurator.include('khufu.pyrasqlalchemy')``
  2. Wrap the web app in the SQLAHelper middleware with
     ``khufu.pyrasqlalchemy.with_db(pyramid_app)``

Once inside a SQLAHelper-wrapped application, the database session is
accessed via ``request.db``.

An example which sets up a new wsgi app wrapped in the ``khufu.pyrasqlalchemy``
middlewares... the database connection is built based on the :term:`sqlalchemy.url` value:

.. code-block:: python
 :linenos:

 config = Configurator(root_factory=models.get_root,
                       settings={'sqlalchemy.url': 'sqlite://:memory'})
 config.include('khufu.pyrasqlalchemy')
 app = khufu.pyrasqlalchemy.with_db(config.make_wsgi_app())  

Once inside view code, database queries can happen as follows:

.. code-block:: python
 :linenos:

 @view_config(context=models.SomeContainerModel)
 def users_view(request):
     return {'models': request.db.query(models.SomeModel).all()}

*NOTE: view code should never manually commit the ``request.db`` object,
please use the transaction api directly if this is required*

Database Traversal Utils
------------------------

The following provides traversal as follows::

  /                                 # Root
  /distros/                         # Distribution container
  /distros/foobar                   # Distribution called foobar
  /distros/foobar/versions/         # Versions container for foobar
  /distros/foobar/versions/0.1      # Version 0.1 of foobar

The example code is as follows:

.. code-block:: python
 :linenos:

 from pysoftcenter import models
 from pysoftcenter.traversalutils import (DataContainer,
                                          attrs_traversable,
                                          TraversalMixin)

 class DistroVersionContainer(DataContainer):
     model_class = models.DistroVersion
     unique_lookup = 'version'

 @attrs_traversable(versions=DistroVersionContainer)
 class DistroDataContainer(DataContainer):
     model_class = models.Distro

 class Root(TraversalMixin, dict):
     def __init__(self, db):
         TraversalMixin.__init__(self, db=db)
         self['distros'] = DistroDataContainer('distros', self)

 def get_root(request):
     root = Root(request.db)
     return root


Transaction Handling
====================

If your application requires control over the transaction handling,
please use the :term:`transaction` api.

Under the Hood
==============

There is nothing magical about :term:`Khufu-PyraSQLAlchemy`.  It does the
following things:

  1. Registers a :term:`SQLAlchemy` based session factory and stores it in the middleware
  2. Uses :term:`zope.sqlalchemy` to connect that session factory to the transaction handling
  3. Uses middleware to do the following:

    i) At the start of a request, a new session is created and stuffed into the :term:`environ`
    ii) Using a :term:`NewRequest` event, the active session is retrieved from :term:`environ` and
        added onto the request as the ``db`` attribute.
    iii) At the end of the request, either commit the session/transaction if
         no error occurred, else rollback (provided by :term:`repoze.tm2`).

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