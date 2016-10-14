#!/usr/bin/env python
from setuptools import setup, find_packages
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-s3-folder-storage',
    version='0.5',
    description="Quick extension of django-storages' S3BotoStorage to allow separate folders for uploaded and static media within an S3 bucket.",
    author='Benjamin W Stookey',
    author_email='ben.stookey@gmail.com',
    url='https://github.com/jamstooks/django-s3-folder-storage',
    long_description=read("README.md"),
    packages=[
        's3_folder_storage',
        's3_folder_storage.tests',
        's3_folder_storage.tests.testapp'
        ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    install_requires=['django-storages', 'boto3'],
)
