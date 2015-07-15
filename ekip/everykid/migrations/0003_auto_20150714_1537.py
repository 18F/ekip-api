# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('everykid', '0002_auto_20150713_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='educator',
            name='org_or_school',
            field=models.CharField(choices=[('O', 'Qualified organization'), ('S', 'School')], max_length=1, default='S'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='educator',
            name='address_line_1',
            field=models.CharField(verbose_name='Address line 1', max_length=128),
        ),
        migrations.AlterField(
            model_name='educator',
            name='address_line_2',
            field=models.CharField(null=True, verbose_name='Address line 2', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='educator',
            name='city',
            field=models.CharField(verbose_name='City', max_length=50),
        ),
        migrations.AlterField(
            model_name='educator',
            name='name',
            field=models.CharField(verbose_name='Full name', max_length=128),
        ),
        migrations.AlterField(
            model_name='educator',
            name='num_students',
            field=models.IntegerField(help_text='Number of students for which you are requesting vouchers', verbose_name='Number of students'),
        ),
        migrations.AlterField(
            model_name='educator',
            name='organization_name',
            field=models.CharField(verbose_name='School or organization name', max_length=128),
        ),
        migrations.AlterField(
            model_name='educator',
            name='state',
            field=localflavor.us.models.USStateField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], verbose_name='State', max_length=2),
        ),
        migrations.AlterField(
            model_name='educator',
            name='work_email',
            field=models.CharField(null=True, verbose_name='Work email address', max_length=128),
        ),
        migrations.AlterField(
            model_name='educator',
            name='zipcode',
            field=localflavor.us.models.USZipCodeField(verbose_name='ZIP code', max_length=10),
        ),
    ]
