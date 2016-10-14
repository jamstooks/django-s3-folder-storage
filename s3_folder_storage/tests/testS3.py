"""
    Some tests to make sure that django-s3-folder-storage is storing uploaded
    files to S3 as expected.

    Designed to be run within a project to confirm that settings are correctly
    set up.
"""

import string
import random
import requests
import sys
import time

from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from s3_folder_storage.s3 import DefaultStorage, StaticStorage

__all__ = (
    'ConfigurationTest',
)


class ConfigurationTest(TestCase):

    def setUp(self):
        """
            Generate a random string to test in the file content
        """
        chars = string.ascii_uppercase + string.digits
        self.file_text = ''.join(random.choice(chars) for x in range(6))
        self.file_text = "Dummy Test: %s" % self.file_text
        self.VERBOSE = False

    def testMediaUpload(self):
        """
            Upload a file and then confirm that it was uploaded
            for Media and Static files
        """
        self._testUpload(DefaultStorage(), 'media')
        self._testUpload(StaticStorage(), 'static')

    def _testUpload(self, storage, folder):

        # upload a file
        name = 's3dummyfile.txt'
        content = ContentFile(self.file_text)
        storage.save(name, content)

        if self.VERBOSE:
            print
            print "Write: %s/%s" % (folder, name)
            print "Content: '%s'" % self.file_text

        # confirm it was uploaded
        f = storage.open(name, 'r')
        file_text = f.read()
        self.assertEqual(file_text, self.file_text)

        if self.VERBOSE:
            print "Read: %s" % f.key.name
            print >> sys.stdout, "Content: '%s'" % file_text

        self.assertEqual(f.obj.key, "%s/%s" % (folder, name))
        f.close()

        if self.VERBOSE:
            print "cleaning up: deleting file: %s" % f.key.name

        # cleanup
        f.obj.delete()

    def testFileField(self):
        """
            Tests that a FileField on a Model is stored properly
        """
        filename = 'test_file_%s.txt' % str(time.time()).split('.')[0]

        from s3_folder_storage.tests.testapp.models import TestModel
        my_model = TestModel()
        my_model.upload = SimpleUploadedFile(filename, 'blahblah')
        my_model.save()

        # make sure it's saved on the model correctly
        self.assertRegexpMatches(my_model.upload.url, ".*/media/%s" % filename)

        # test the file is reachable
        response = requests.get(my_model.upload.url)
        self.assertEqual(response.status_code, 200)

        # clean up
        f = my_model.upload.storage.open(filename, 'r')
        f.obj.delete()
