.. -*-rst-*-

==================
 Khufu-SQLAHelper
==================

Khufu-SQLAHelper is meant to reduce the plumbing required to configure an
active SQLAlchemy-based database connection with a web app.


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

Credits
=======

  * Developed and maintained by Rocky Burt <rocky AT serverzen DOT com>
