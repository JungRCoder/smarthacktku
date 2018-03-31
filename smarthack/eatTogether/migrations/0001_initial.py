# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-31 12:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=225, null=True, unique=True)),
                ('day', models.DateTimeField(blank=True, default=datetime.datetime(2018, 3, 31, 20, 8, 22, 942555))),
                ('place', models.CharField(blank=True, max_length=225, null=True)),
                ('count', models.IntegerField(blank=True, default='0', null=True)),
                ('pw', models.CharField(blank=True, max_length=225, null=True)),
                ('comment', models.TextField(blank=True, max_length=225, null=True)),
            ],
        ),
    ]
