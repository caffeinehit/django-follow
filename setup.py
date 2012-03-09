#!/usr/bin/env python

from setuptools import setup, find_packages
import follow

setup(
    name='django-follow',
    description='Application which enables following features for users. Can be used for contact books or whatnot',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-follow',
    include_package_data=True,
    package_data={'follow': ['templates/follow/*html']},
    zip_safe=False,
    version=follow.__version__,
)
