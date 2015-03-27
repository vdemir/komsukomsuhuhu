# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entities', '0004_topic_user_favorited'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_displayed_posts',
            field=models.ManyToManyField(related_name='read_posts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
