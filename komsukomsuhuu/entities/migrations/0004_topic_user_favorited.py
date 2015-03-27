# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entities', '0003_auto_20150319_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='user_favorited',
            field=models.ManyToManyField(related_name='favorite_topic', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
