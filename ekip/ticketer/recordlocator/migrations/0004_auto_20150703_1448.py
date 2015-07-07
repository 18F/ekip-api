# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0004_federalsite_slug'),
        ('recordlocator', '0003_auto_20150610_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recreation_site', models.ForeignKey(to='nationalparks.FederalSite')),
            ],
        ),
        migrations.AlterField(
            model_name='ticket',
            name='redeemed',
            field=models.ForeignKey(blank=True, null=True, to='recordlocator.Redemption'),
        ),
        migrations.DeleteModel(
            name='RedemptionLocation',
        ),
    ]
