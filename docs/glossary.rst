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

   repoze.tm2
     `repoze.tm2 <http://docs.repoze.org/tm2/>`_ provides middleware to
     help with transactions.

   pyramid_traversalwrapper
     `pyramid_traversalwrapper distribution <http://pypi.python.org/pypi/pyramid_traversalwrapper>`_
     provides proxy wrappers for objects.

   Khufu-PyraSQLAlchemy
     `Khufu-PyraSQLAlchemy <https://github.com/serverzen/Khufu-PyraSQLAlchemy>`_ 
     is meant to reduce the plumbing required to configure a :term:`SQLAlchemy`
     based database connection with a :term:`Pyramid` based web app.

   environ
     The standard ``dict`` object passed into a WSGI callable.

   NewRequest
     The event fired before each and every :term:`Pyramid` request, see
     `NewRequest API docs
     <http://docs.pylonsproject.org/projects/pyramid/1.0/api/events.html#pyramid.events.NewRequest>`_
     for further details.

   sqlalchemy.url
     The ``settings`` key used to derive a :term:`SQLAlchemy` engine from.
