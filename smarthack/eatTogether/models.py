# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models


# Create your models here.
class Invite(models.Model):
    title = models.CharField(max_length=225, null=True, blank=True,  unique=True)
    day = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    place = models.CharField(max_length=225, null=True, blank=True)
    count = models.IntegerField(default="0", null=True, blank=True)
    pw = models.CharField(max_length=225, null=True, blank=True)
    comment = models.TextField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return self.title