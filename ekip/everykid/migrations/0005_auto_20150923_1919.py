# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('everykid', '0004_auto_20150818_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educator',
            name='num_students',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)], help_text='Number of students for which you are requesting vouchers', verbose_name='Number of students'),
        ),
    ]
