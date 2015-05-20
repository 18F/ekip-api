# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedemptionLocation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('zip_code', models.CharField(max_length=5)),
                ('record_locator', models.CharField(max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('redeemed', models.ForeignKey(to='recordlocator.RedemptionLocation', blank=True, null=True)),
            ],
        ),
    ]
