# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0010_auto_20150902_1902'),
        ('recordlocator', '0005_auto_20150703_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalRedemption',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('redemption_entry', models.DateTimeField(auto_now_add=True)),
                ('recreation_site', models.ForeignKey(to='nationalparks.FederalSite')),
                ('ticket', models.ForeignKey(to='recordlocator.Ticket')),
            ],
        ),
    ]
