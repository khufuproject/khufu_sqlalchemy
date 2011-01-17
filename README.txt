.. -*-rst-*-

==================
 Khufu-SQLAHelper
==================

Khufu-SQLAHelper is meant to reduce the plumbing required to configure a
SQLAlchemy_ based database connection with a Pyramid_ based web app.


Requirements
============

  * Python 2.6 or 2.7 (not tested with Python 3.x)
  * SQLAlchemy
  * zope.sqlalchemy
  * repoze.tm2


Usage
=====

To use SQLAHelper there are two steps:

  1. Hook up the configuration via ``sqlahelper.init_config(configurator)``
  2. Wrap the web app in the SQLAHelper middleware with
     ``sqlahelper.with_db(app, 'sqlite:///:memory')``

An example::

    config = Configurator(root_factory=models.get_root,
                          settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
  
  

Credits
=======

  * Developed and maintained by Rocky Burt <rocky AT serverzen DOT com>

.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/
