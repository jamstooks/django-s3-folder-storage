django-s3-folder-storage
========================

[![Latest PyPI version](https://pypip.in/v/django-s3-folder-storage/badge.png)](https://crate.io/packages/django-s3-folder-storage/)
[![Number of PyPI downloads](https://pypip.in/d/django-s3-folder-storage/badge.png)](https://crate.io/packages/django-s3-folder-storage/)


Quick extension of django-storages' [S3BotoStorage](http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html) to allow separate folders for uploaded and static media within an S3 bucket.

Overview
--------

Many of my sites use the same configuration: **static** files are stored in `//s3.amazonaws.com/<bucket_name>/static/` and **uploaded** files are stored somewhere under `//s3.amazonaws.com/<bucket_name>/media/`. Instead of extending S3BotoStorage in every project I decided to build a package. The names of those folders are configurable in `settings.py`.

Installation
------------

Use `pip` to install from PyPI:

	pip install django-s3-folder-storage

Add `s3_folder_storage` to your settings.py file:

	INSTALLED_APPS = (
	    ...
	    's3_folder_storage',
	    ...
	)

Configuration
-------------

You are essentially using `django-storages` for S3 hosting, so you will be using their settings. The two settings that are specific to `django-s3-folder-storage` are `DEFAULT_S3_PATH` and `STATIC_S3_PATH`.

Here's an example:

	DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
	DEFAULT_S3_PATH = "media"
	STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
	STATIC_S3_PATH = "static"
	AWS_ACCESS_KEY_ID = {{ your key id here }}
	AWS_SECRET_ACCESS_KEY = {{ your secret key here }}
	AWS_STORAGE_BUCKET_NAME = {{ your bucket name here }}
	
	MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
	MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
	STATIC_ROOT = "/%s/" % STATIC_S3_PATH
	STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
	ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
	
Contributing
------------

Think this needs something else? To contribute to `django-s3-folder-storage` create a fork on github. Clone your fork, make some changes, and submit a pull request.

Bugs are great contributions too! Feel free to add an issue on github.
