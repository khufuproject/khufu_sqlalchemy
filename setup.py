import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid_tm',
    'setuptools',
    'SQLAlchemy >= 0.6.1',
    'zope.sqlalchemy',
    ]

setup(name='khufu_sqlalchemy',
      version='0.5b1',
      description='SQLAlchemy bindings for Pyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        ],
      license='BSD',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      url='https://github.com/serverzen/khufu_sqlalchemy',
      keywords='pyramid sqlalchemy khufu transaction',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite="khufu_sqlalchemy.tests",
      entry_points='',
      )
