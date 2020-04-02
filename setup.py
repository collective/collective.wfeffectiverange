# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


version = '2.0.1.dev0'
shortdesc = 'Workflowed effective range (Plone/Dexterity)'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENCE.rst')).read()

setup(
    name='collective.wfeffectiverange',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='workflow cms security zope plone publication date',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://pypi.python.org/pypi/collective.wfeffectiverange',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFPlone',
        'plone.api',
        'plone.app.dexterity',
        'plone.app.event',
        'plone.app.vocabularies',
        'plone.app.z3cform',
        'plone.autoform > 1.6.0',
        'plone.indexer',
        'plone.protect',
        'plone.supermodel',
        'setuptools',
        'z3c.form >= 3.2.1',
        'z3c.relationfield',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'interlude[ipython]>=1.3.1',
            'plone.app.contenttypes',  # for local testing
            'plone.app.robotframework [debug]',
            'plone.app.testing',
        ],
    },
    entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
    """,
)
