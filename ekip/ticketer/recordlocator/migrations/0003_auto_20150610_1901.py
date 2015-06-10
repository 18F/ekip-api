# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordlocator', '0002_auto_20150602_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='record_locator',
            field=models.CharField(max_length=16),
        ),
    ]
