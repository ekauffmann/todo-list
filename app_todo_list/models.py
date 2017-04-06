from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Task(models.Model):
    text = models.TextField()
    state = models.IntegerField(default=0)
    