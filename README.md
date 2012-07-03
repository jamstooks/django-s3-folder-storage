django-s3-folder-storage
========================

Quick extension of django-storages' S3BotoStorage to allow separate folders for uploaded and static media within an S3 bucket.

Installation
------------

Use `pip` to install from github (until I get this on PyPI):

	pip install -e git://github.com/jamstooks/django-s3-folder-storage.git#egg=django_s3_folder_storage-dev

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