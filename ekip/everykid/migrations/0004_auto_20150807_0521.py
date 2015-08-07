# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('everykid', '0003_auto_20150714_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educator',
            name='name',
            field=models.CharField(max_length=128, verbose_name="Educator's full name"),
        ),
        migrations.AlterField(
            model_name='educator',
            name='org_or_school',
            field=models.CharField(max_length=1, choices=[('S', 'School'), ('O', 'Qualified organization')], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='educator',
            name='zipcode',
            field=localflavor.us.models.USZipCodeField(max_length=10, verbose_name='Zip'),
        ),
    ]
