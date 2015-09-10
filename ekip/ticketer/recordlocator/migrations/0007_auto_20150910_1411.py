# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordlocator', '0006_additionalredemption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='record_locator',
            field=models.CharField(db_index=True, max_length=16),
        ),
    ]
