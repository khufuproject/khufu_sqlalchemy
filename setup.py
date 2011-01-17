import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['setuptools',
            'SQLAlchemy >= 0.6.1',
            'repoze.tm2',
            'zope.sqlalchemy']

setup(name='Khufu-SQLAHelper',
      version='0.2.1',
      description='Khufu component for using SQLAlchemy with Pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        ],
      license='BSD',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      namespace_packages=['khufu'],
      url='http://bitbucket.org/rockyburt/khufu-sqlahelper',
      keywords='web pyramid sqlalchemy',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite="khufu.sqlahelper.tests",
      entry_points="",
      )
