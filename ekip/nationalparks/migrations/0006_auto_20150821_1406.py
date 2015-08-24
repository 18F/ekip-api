# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0005_auto_20150818_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtripsite',
            name='city',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
