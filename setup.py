#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0', 'requests', 'numpy', 'scikit-learn', 'keras', 'falcon',
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(rcourivaud): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='query_categorizer',
    version='0.1.0',
    description="Python project used to categorize short queries",
    long_description=readme + '\n\n' + history,
    author="Raphaël Courivaud",
    author_email='r.courivaud@qwant.com',
    url='https://github.com/rcourivaud/query_categorizer',
    packages=find_packages(include=['query_categorizer']),
    entry_points={
        'console_scripts': [
            'query_categorizer=query_categorizer.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='query_categorizer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
