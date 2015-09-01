import os
import sys
import django

BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.exc_clear()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        's3_folder_storage',
    )
    if django.VERSION > (1, 2):
        global_settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_PATH, 'connpass.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
    else:
        global_settings.DATABASE_ENGINE = "sqlite3"
        global_settings.DATABASE_NAME = ":memory:"

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'beproud.django.authutils.middleware.AuthMiddleware',
    )

    # custom settings for tests
    global_settings.DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    global_settings.DEFAULT_S3_PATH = "media"
    global_settings.STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    global_settings.STATIC_S3_PATH = "static"

    # requires some envifonment variables
    global_settings.AWS_ACCESS_KEY_ID = os.environ.get(
        'AWS_ACCESS_KEY_ID', None)
    global_settings.AWS_SECRET_ACCESS_KEY = os.environ.get(
        'AWS_SECRET_ACCESS_KEY', None)
    global_settings.AWS_STORAGE_BUCKET_NAME = os.environ.get(
        'AWS_STORAGE_BUCKET_NAME', None)

    global_settings.MEDIA_ROOT = '/%s/' % global_settings.DEFAULT_S3_PATH
    global_settings.MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % global_settings.AWS_STORAGE_BUCKET_NAME
    global_settings.STATIC_ROOT = "/%s/" % global_settings.STATIC_S3_PATH
    global_settings.STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % global_settings.AWS_STORAGE_BUCKET_NAME
    global_settings.ADMIN_MEDIA_PREFIX = global_settings.STATIC_URL + 'admin/'

    # global_settings.DEFAULT_FILE_STORAGE = 'backends.s3boto.S3BotoStorage'
    # global_settings.AWS_IS_GZIPPED = True
    global_settings.SECRET_KEY = "blahblah"

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 7):
        print "running 1.7+ tests"
        django.setup()
        from django.test.runner import DiscoverRunner
        test_runner = DiscoverRunner()
        failures = test_runner.run_tests(['s3_folder_storage', ])
    elif django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['s3_folder_storage', ])
    else:
        failures = test_runner(['s3_folder_storage', ], verbosity=1)
    sys.exit(failures)

if __name__ == '__main__':
    main()
