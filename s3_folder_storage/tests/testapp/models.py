from django.db import models


class TestModel(models.Model):
    upload = models.FileField()
