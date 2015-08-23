# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0006_auto_20150821_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtripsite',
            name='address_line_1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtripsite',
            name='zipcode',
            field=localflavor.us.models.USZipCodeField(max_length=10, null=True),
        ),
    ]
