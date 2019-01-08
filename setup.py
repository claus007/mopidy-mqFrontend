from __future__ import absolute_import, unicode_literals

import re
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-MqFrontEnd',
    version=get_version('mopidy_mqFrontend/__init__.py'),
    url='https://github.com/claus007/mopidy-mqFrontend',
    license='Apache License, Version 2.0',
    author='Claus Ilginnis',
    author_email='Claus@Ilginnis.de',
    description='Forward Information to an MQTT Broker',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.14',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'soundspot = mopidy_mqFrontend:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Frontend',
    ],
)
