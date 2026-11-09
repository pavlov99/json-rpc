#!/usr/bin/env python
import os.path
import sys
from setuptools import setup, find_packages
from jsonrpc import version


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup_requires = ["pytest-runner"] if sys.argv in ['pytest', 'test'] else []

setup(
    name="json-rpc",
    version=version,
    packages=find_packages(),
    setup_requires=setup_requires,
    tests_require=["pytest"],
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*",

    # metadata for upload to PyPI
    author="Kirill Pavlov",
    author_email="k@p99.io",
    url="https://github.com/pavlov99/json-rpc",
    description="JSON-RPC transport implementation",
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",

    # Full list:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)
