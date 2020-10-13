#!/usr/bin/env python
from setuptools import setup, find_packages
import re
import os


def get_version():
    fn = os.path.join(os.path.dirname(__file__), "scrapy_ninja_requests", "__init__.py")
    with open(fn) as f:
        return re.findall("__version__ = '([\d.\w]+)'", f.read())[0]


def get_long_description():
    readme = open('README.md').read()
    return readme


setup(
    name='scrapy-ninja-requests',
    version=get_version(),
    author='Francois Liot',
    author_email='francois@liot.org',
    license='MIT license',
    long_description=get_long_description(),
    description="Rotating proxies for Requests session",
    url='https://github.com/fliot/scrapy-ninja-requests',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'fake-useragent',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Framework :: Scrapy',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
