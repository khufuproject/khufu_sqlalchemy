Changes
=======

0.5.3 (Jul-10-2011)
-------------------

  * now tries to make sure the active context is part of the active db session

  * Various fixes to make session lookup more rigourous

0.5.2 (Jul-10-2011)
-------------------

  * Small fixes

0.5.1 (May-14-2011)
-------------------

  * Fixed bad import in the paster template

  * Put in hack to work around bug with connection pooling and sqlite
    https://github.com/Pylons/pyramid/issues/174

  * Now uses scoped_session for session factory by default

  * sessions created by ``dbsession()`` are now closed upon finishing the
    request

0.5 (May-04-2011)
-----------------

  * Added new *khufu_sqlalchemy* paster template

  * Made dbsession() lookup a little more clever

0.5b1 (Feb-28-2011)
-------------------

  * Backwards incompat changes with 0.4, please stay with 0.4
    to continue using middleware

  * Now uses ``khufu_sqlalchemy.dbsession(request)`` for getting
    the active db session

  * ``traversalutils`` was moved out (in preparation for another
    package

0.4a4 (Feb-20-2011)
-------------------

  * Renamed from Khufu-SQLAHelper to khufu_sqlalchemy

0.4a3 (Feb-16-2011)
-------------------

  * Updated project url's

0.4a2 (Feb-11-2011)
-------------------

  * Fixed small issue where decorator wasn't working

0.4a1 (Feb-10-2011)
-------------------

  * Added traversalutils for helping expose SQL-based models
    using traversal 

0.3 (Feb-04-2011)
-----------------

  * Changed ``with_db`` api to make db param optional

  * Updated docs

0.2.1 (Jan-17-2011)
-------------------

  * Added ``use_zope_tm`` option to ``get_session_factory``

0.2 (Jan-9-2011)
----------------

  * first release
