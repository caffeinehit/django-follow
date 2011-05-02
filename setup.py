#!/usr/bin/env python

from setuptools import setup,find_packages

setup(
    name='django-follow',
    description='Application which enables following features for users. Can be used for contact books or whatnot',
    long_description=open('README.rst').read(),
    packages=['follow'],
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-follow',
    version='0.3',
)
