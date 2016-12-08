from setuptools import setup, find_packages
import os

version = '1.8.1'
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
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='',
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
        'Plone',
        'plone.api',
        'plone.app.vocabularies',
        'plone.autoform > 1.6.0',
        'setuptools',
        'z3c.form >= 3.2.1',
        'plone.protect',
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
