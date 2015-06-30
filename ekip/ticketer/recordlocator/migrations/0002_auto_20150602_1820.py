# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('recordlocator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='zip_code',
            field=localflavor.us.models.USZipCodeField(max_length=10),
        ),
    ]
