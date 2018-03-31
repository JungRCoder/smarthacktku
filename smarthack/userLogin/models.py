# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fullName = models.CharField(max_length=128)
    checkVerify = models.BooleanField(default=False)
    verifyEmailCode = models.CharField(max_length=4)
    def __str__(self):
        return self.fullName + ' (' + self.user.username + ')'