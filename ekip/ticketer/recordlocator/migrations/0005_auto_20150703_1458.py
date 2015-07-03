# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0004_federalsite_slug'),
        ('recordlocator', '0004_auto_20150703_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redemption',
            name='recreation_site',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='redeemed',
        ),
        migrations.AddField(
            model_name='ticket',
            name='recreation_site',
            field=models.ForeignKey(null=True, to='nationalparks.FederalSite'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='redemption_entry',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='Redemption',
        ),
    ]
