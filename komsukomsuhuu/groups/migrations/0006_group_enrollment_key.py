# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20150430_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='enrollment_key',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
    ]
