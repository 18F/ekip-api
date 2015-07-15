# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('everykid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='educator',
            name='num_students',
            field=models.IntegerField(default=0, help_text='Number of students for which you are requesting vouchers'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educator',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
