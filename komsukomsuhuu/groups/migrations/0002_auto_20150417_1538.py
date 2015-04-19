# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('group', models.OneToOneField(to='groups.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='group',
            name='user_favorited',
            field=models.ManyToManyField(related_name='favorite_groups', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
