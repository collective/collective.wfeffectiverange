from setuptools import setup, find_packages
import os

version = '1.0'
shortdesc = 'Workflows timed by effective range (Plone/Dexterity)'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc = open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

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
    url=u'https://bluedynamics.com',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Plone',
        'plone.api',
        'z3c.form >= 3.2.1',
        'plone.app.vocabularies',
        'Products.cron4plone',
        ,
    ],
    extras_require={
        'test': [
            'interlude[ipython]>=1.3.1',
            'ipdb',
            'plone.app.testing',
            'plone.app.robotframework [debug]',
            #for local testing
            'plone.app.contenttypes',
        ],
    },
    entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
    """,
)
