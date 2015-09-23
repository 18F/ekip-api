# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('everykid', '0005_auto_20150923_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educator',
            name='num_students',
            field=models.IntegerField(help_text='Number of students for which you are requesting vouchers', validators=[django.core.validators.MaxValueValidator(50, 'You can only print up to 50 passes at a time.'), django.core.validators.MinValueValidator(1, 'You can not print less than one pass.')], verbose_name='Number of students'),
        ),
    ]
