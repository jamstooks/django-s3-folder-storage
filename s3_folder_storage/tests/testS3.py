"""
    Some tests to make sure that django-s3-folder-storage is storing uploaded
    files to S3 as expected.
    
    Designed to be run within a project to confirm that settings are correctly
    set up.
"""

import string
import random
import sys
import os

from django.test import TestCase
from django.core.files.base import ContentFile

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
        
        self.assertEqual(f.key.name, "%s/%s" % (folder, name))
        f.close()
        
        if self.VERBOSE:
            print "cleaning up: deleting file: %s" % f.key.name
        storage.bucket.delete_key(f.key)
        
        # # print >> sys.stdout, os.path.abspath(f)
        # print f.__dict__.keys()
        # print f.name
        # print f.key.__dict__.keys()
        # print "key: %s" % f.key
        # print "path: %s" % f.key.path
        # print "name: %s" % f.key.name