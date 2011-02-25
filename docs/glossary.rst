.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Pyramid
      `Pyramid <http://pylonshq.com/pyramid>`_ is a small, fast, down-to-earth
      Python web application development framework.

   SQLAlchemy
      An `Object relational framework <http://www.sqlalchemy.org/>`_.

   transaction
      A database transaction comprises a unit of work performed within a
      database management system.  Within this context it is also the
      name of a `Python distribution <http://pypi.python.org/pypi/transaction>`_.

   zope.sqlalchemy
      `zope.sqlalchemy <http://pypi.python.org/pypi/zope.sqlalchemy>`_
      connects :term:`SQLAlchemy` to general purpose
      :term:`transaction` machinery

   khufu_sqlalchemy
     `khufu_sqlalchemy <https://github.com/serverzen/khufu_sqlalchemy>`_ 
     is meant to reduce the plumbing required to configure a :term:`SQLAlchemy`
     based database connection with a :term:`Pyramid` based web app.

   environ
     The standard ``dict`` object passed into a WSGI callable.

   sqlalchemy.url
     The ``settings`` key used to derive a :term:`SQLAlchemy` engine from.

   engine
     The :term:`SQLAlchemy` database engine being used, see `Engine Configuration
     <http://www.sqlalchemy.org/docs/core/engines.html>`_ for further details.

   session factory
     The :term:`SQLAlchemy` database session factory being used, see `Using
     the Session <http://www.sqlalchemy.org/docs/orm/session.html>`_ for
     further details.

   pyramid_tm
     :term:`Transaction` handling based on the :term:`transaction` package.
