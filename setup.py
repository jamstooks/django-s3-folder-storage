#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-s3-folder-storage',
    version='0.1',
    description="Quick extension of django-storages' S3BotoStorage to allow separate media and static folders within a bucket.",
    author='Benjamin W Stookey',
    author_email='ben.stookey@gmail.com',
    url='https://github.com/jamstooks/django-s3-folder-storage',
    long_description=read("README.md"),
    packages=['s3_folder_storage']
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ],
    install_requires=['django-storages'],
)