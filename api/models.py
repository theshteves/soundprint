from __future__ import unicode_literals

from django.db import models

class Sound(models.Model):
    soundprint = models.FileField(max_length=64)
    message = models.CharField(max_length=512)

