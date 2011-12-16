import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = ['pyramid', 'WebError', 'pymongo', 'deform', 'pyzmq', 'msgpack-python', 'pyramid_beaker', 'mongoengine']

setup(name='triage',
      version='0.0',
      description='triage',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Niall O'Higgins",
      author_email='nialljohiggins@gmail.com',
      url='https://github.com/niallo/pyramid_mongodb',
      keywords='web pyramid pylons mongodb',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="triage",
      entry_points="""\
      [paste.app_factory]
      main = triage:main
      """,
      paster_plugins=['pyramid'],
      )

