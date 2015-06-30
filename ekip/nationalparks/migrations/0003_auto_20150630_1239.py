# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0002_auto_20150624_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='federalsite',
            name='site_type',
            field=models.CharField(choices=[('NPS', 'National Park Service'), ('NWR', 'National Wildlife Refuge'), ('BLM', 'Bureau of Land Management'), ('NF', 'National Forest'), ('NRA', 'National Recreation Area'), ('NHS', 'National Historic Site'), ('OTH', 'Other')], max_length=3),
        ),
    ]
