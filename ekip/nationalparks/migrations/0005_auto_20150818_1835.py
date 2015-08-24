# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('nationalparks', '0004_federalsite_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestVisitTime',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('best_time', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='FieldTripSite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('agency', models.CharField(choices=[('USACE', 'US Army Corps of Engineers'), ('BLM', 'Bureau of Land Management'), ('USBR', 'Bureau of Reclamation'), ('NOAA', 'National Oceanic and Atmospheric Administration'), ('NPS', 'National Park Service'), ('FWS', 'U.S. Fish and Wildlife Service'), ('FS', 'U.S. Forest Service')], max_length=5)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, max_length=20)),
                ('phone_extension', models.IntegerField(null=True)),
                ('city', models.CharField(max_length=128)),
                ('state', localflavor.us.models.USStateField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('website', models.URLField(max_length=512)),
                ('slug', models.SlugField(unique=True, null=True)),
                ('address_line_1', models.CharField(max_length=256)),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10)),
                ('advance_reservation', models.BooleanField(default=False, help_text='If advance reservation for large groups is required.')),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('larger_groups', models.BooleanField(default=True, help_text='If the site can accomodate more than 35 4th graders.')),
                ('best_visit_times', models.ManyToManyField(to='nationalparks.BestVisitTime')),
            ],
        ),
        migrations.CreateModel(
            name='YouthFacility',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('facility', models.CharField(unique=True, max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='fieldtripsite',
            name='facilities',
            field=models.ManyToManyField(to='nationalparks.YouthFacility'),
        ),
        migrations.AlterUniqueTogether(
            name='fieldtripsite',
            unique_together=set([('name', 'agency')]),
        ),
    ]
