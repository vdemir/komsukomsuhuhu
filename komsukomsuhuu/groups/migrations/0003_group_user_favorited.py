# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0002_grouplocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='user_favorited',
            field=models.ManyToManyField(related_name='favorite_groups', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
