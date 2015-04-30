# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_group_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='duration',
            field=models.IntegerField(default=0, choices=[(0, b'permanent'), (1, b'1 hour'), (2, b'2 hour'), (3, b'3 hour'), (4, b'4 hour'), (5, b'5 hour'), (6, b'6 hour'), (7, b'7 hour'), (8, b'8 hour'), (9, b'9 hour'), (10, b'10 hour'), (11, b'11 hour'), (12, b'12 hour'), (13, b'13 hour'), (14, b'14 hour'), (15, b'15 hour'), (16, b'16 hour'), (17, b'17 hour'), (18, b'18 hour'), (19, b'19 hour'), (20, b'20 hour'), (21, b'21 hour'), (22, b'22 hour'), (23, b'23 hour'), (24, b'24 hour')]),
            preserve_default=True,
        ),
    ]
