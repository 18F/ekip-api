# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0009_auto_20150831_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='federalsite',
            name='active_participant',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='federalsite',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True, default=timezone.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='federalsite',
            name='version',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
