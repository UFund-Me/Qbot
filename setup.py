#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# qbot - AI automatic quant trader bot
# https://github.com/UFund-Me/Qbot

"""qbot - AI automatic quant trader bot"""

from setuptools import setup, find_packages
# from codecs import open
import io
from os import path

# --- get version ---
version = "0.1.1"
with open("qbot/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')
# --- /get version ---


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qbot',
    version=version,
    description='AI automatic quant trader bot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/UFund-Me/Qbot',
    author='Charmve',
    author_email='yidazhang1@gmail.com',
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    platforms=['any'],
    keywords='quant, finteck, AI, trader',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['pandas>=1.3.0', 'numpy>=1.16.5',
                      'requests>=2.26', 'multitasking>=0.0.7',
                      'lxml>=4.9.1', 'appdirs>=1.4.4', 'pytz>=2022.5',
                      'frozendict>=2.3.4', 
                      # 'pycryptodome>=3.6.6',
                      'cryptography>=3.3.2',
                      'beautifulsoup4>=4.11.1', 'html5lib>=1.1'],
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)

print("""
NOTE: qbot is not affiliated, endorsed, or vetted by Yahoo, Inc.

You should refer to Yahoo!'s terms of use for details on your rights
to use the actual data downloaded.""")