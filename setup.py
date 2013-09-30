import os
from setuptools import setup, find_packages
from jsonrpc import version

# Import multiprocessing to prevent test run problem. In case of nosetests
# (not nose2) there is probles, for details see:
# https://groups.google.com/forum/#!msg/nose-users/fnJ-kAUbYHQ/_UsLN786ygcJ
# http://bugs.python.org/issue15881#msg170215w
try:
    import multiprocessing
except ImportError:
    pass


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""

install_requires = read("requirements.txt").split()

setup(
    name="json-rpc",
    version=version,
    packages=find_packages(),
    # test_suite="nose2.collector.collector",
    test_suite="nose.collector",
    tests_require=["nose"],

    # metadata for upload to PyPI
    author="Kirill Pavlov",
    author_email="kirill.pavlov@phystech.edu",
    url="https://github.com/pavlov99/json-rpc",
    description="JSON-RPC transport realisation",

    # Full list:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
