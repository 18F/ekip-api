# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0003_auto_20150630_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='federalsite',
            name='slug',
            field=models.SlugField(unique=True, null=True),
        ),
    ]
