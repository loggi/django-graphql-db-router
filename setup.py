#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requirements = [
    'Django>=1.8,<2.2.25',
]

setup_requirements = []

setup(
    name='django-graphql-db-router',
    version='0.1',
    packages=find_packages(include=['django-graphql-db-router']),
    description='A Django DB router for GraphQL.',
    long_description=readme,
    author='Loggi Tecnologia',
    author_email='eng@loggi.com',
    url='https://github.com/loggi/django-graphql-db-router',
    license='BSD license',
    install_requires=install_requirements,
    setup_requires=setup_requirements,
)
