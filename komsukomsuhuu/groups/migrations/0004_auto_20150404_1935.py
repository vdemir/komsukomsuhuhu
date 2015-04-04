# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_group_user_favorited'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='range',
            field=models.IntegerField(default=1, choices=[(1, b'1 KM'), (2, b'2 KM'), (3, b'3 KM'), (4, b'4 KM'), (5, b'5 KM')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='state',
            field=models.IntegerField(default=1, choices=[(1, b'Permanent'), (2, b'Temporary')]),
            preserve_default=True,
        ),
    ]
