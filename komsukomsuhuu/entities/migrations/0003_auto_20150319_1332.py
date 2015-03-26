# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20150316_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(related_name='post_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
