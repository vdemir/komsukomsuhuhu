# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20150417_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
