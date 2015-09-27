# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordlocator', '0007_auto_20150910_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'permissions': (('view_exchange_data', 'Can view exchange data'),)},
        ),
    ]
