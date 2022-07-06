#!/usr/bin/env python
# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license.
# See the NOTICE for more information.


from setuptools import setup, find_packages

import glob
from imp import load_source
import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 6, 0, 'final'):
    raise SystemExit("Restkit requires Python 2.6 or later.")

extras = {}

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries']


SCRIPTS = ['scripts/restcli']

def main():
    version = load_source("version", os.path.join("restkit",
        "version.py"))

    # read long description
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()

    DATA_FILES = [
        ('restkit', ["LICENSE", "MANIFEST.in", "NOTICE", "README.rst",
                        "THANKS", "TODO.txt"])
        ]

    options=dict(
            name = 'restkit',
            version = version.__version__,
            description = 'Python REST kit',
            long_description = long_description,
            author = 'Benoit Chesneau',
            author_email = 'benoitc@e-engura.org',
            license = 'MIT',
            url = 'http://benoitc.github.com/restkit',
            classifiers = CLASSIFIERS,
            packages = find_packages(),
            data_files = DATA_FILES,
            scripts = SCRIPTS,
            zip_safe =  False,
            entry_points =  {
                'paste.app_factory': [
                    'proxy = restkit.contrib.wsgi_proxy:make_proxy',
                    'host_proxy = restkit.contrib.wsgi_proxy:make_host_proxy',
                    'couchdb_proxy = restkit.contrib.wsgi_proxy:make_couchdb_proxy',
                ]},
            install_requires = [
                'http-parser>=0.7.7',
                'socketpool>=0.5.0',
                'nose',
                'webob',

                'asn1crypto==0.22.0',
                'async-timeout==4.0.2',
                'atomicwrites==1.4.0',
                'attrs==19.3.0',
                'Automat==20.2.0',
                'certifi==2022.6.15',
                'cffi==1.15.0',
                'charset-normalizer==2.1.0',
                'colorama==0.3.3',
                'constantly==15.1.0',
                'cryptography==37.0.2',
                'decorator==5.1.1',
                'Deprecated==1.2.13',
                'enum34==1.1.10',
                'greenlet==1.1.2',
                'http-parser==0.9.0',
                'hyperlink==18.0.0',
                'idna==2.7',
                'incremental==21.3.0',
                'iniconfig==1.1.1',
                'ipaddress==1.0.18',
                'Jinja2==2.8',
                'logutils==0.3.3',
                'MarkupSafe==0.23',
                'mock==1.0.1',
                'msal==1.17.0',
                'nose==1.3.7',
                'numpy==1.22.4',
                'packaging==21.3',
                'pip==22.0.4',
                'pluggy==1.0.0',
                'prometheus-client==0.12.0',
                'psutil==5.8.0',
                'py==1.11.0',
                'pyasn1==0.3.7'
                'pyasn1-modules==0.1.5',
                'pycparser==2.18',
                'PyHamcrest==1.9.0',
                'PyJWT==2.4.0',
                'pyOpenSSL==17.3.0',
                'pyparsing==3.0.9',
                'pypiwin32==223',
                'pytest==7.1.2',
                'pytest-twisted==1.13.4',
                'python-dateutil==2.4.2',
                'python-ldap==3.4.0',
                'pywin32==304',
                'PyYAML==6.0
                'requests==2.28.1',
                'ruamel.yaml==0.16.13',
                'ruamel.yaml.clib==0.2.2',
                'service-identity==21.1.0',
                'setuptools==60.9.3',
                'setuptools-scm==7.0.4',
                'simplejson==3.17.6',
                'six==1.16.0',
                'socketpool>=0.5.3',
                'tomli==2.0.1',
                'Twisted==22.4.0',
                'twisted-iocpsupport==1.0.2',
                'txredisapi==1.4.4',
                'typing_extensions==4.3.0',
                'ujson==1.22',
                'urllib3==1.26.9',
                'virtualenv==12.1.1',
                'wheel==0.37.1',
                'wrapt==1.14.1',
                'zc.buildout==2.2.1',
                'zope.interface==5.4.0',

            ],
            test_suite = 'nose.collector'
        )


    setup(**options)

if __name__ == "__main__":
    main()
