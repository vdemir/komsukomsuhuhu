# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_group_enrollment_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='enrollment_key',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
