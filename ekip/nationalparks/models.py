from django.db import models
from django.utils.text import slugify

from localflavor.us.models import (
    USStateField, PhoneNumberField, USZipCodeField)


class BestVisitTime(models.Model):
    """ Stores a string that indicates the best time to visit a location. This
    is often expressed as a range such as January - March or Fall through
    Summer. """

    best_time = models.CharField(max_length=128, unique=True)


class YouthFacility(models.Model):
    """ Stores a string that describes a youth facility (activities, features).
    """

    facility = models.CharField(max_length=256, unique=True)


class FieldTripSite(models.Model):
    """ These sites are those that are great for field trips for 4th graders
    (and presumably other ages as well). Internally, this is known as the FICOR
    list. """

    # List of management agencies. 
    AGENCY_CHOICES = (
        ('USACE', 'US Army Corps of Engineers'),
        ('BLM', 'Bureau of Land Management'),
        ('USBR', 'Bureau of Reclamation'),
        ('NOAA', 'National Oceanic and Atmospheric Administration'),
        ('NPS', 'National Park Service'),
        ('FWS', 'U.S. Fish and Wildlife Service'),
        ('FS', 'U.S. Forest Service')
    )

    name = models.CharField(max_length=256)
    agency = models.CharField(max_length=5, choices=AGENCY_CHOICES)
    phone = PhoneNumberField(null=True)
    phone_extension = models.IntegerField(null=True)
    city = models.CharField(max_length=128, null=True)
    state = USStateField(blank=False, null=False)
    website = models.URLField(max_length=512)
    slug = models.SlugField(unique=True, null=True)
    address_line_1  = models.CharField(max_length=256, null=True)
    zipcode = USZipCodeField(null=True)

    advance_reservation = models.BooleanField(
        default=False,
        help_text="If advance reservation for large groups is required.")

    update_timestamp = models.DateTimeField(auto_now=True)

    larger_groups = models.BooleanField(
        default=True, 
        help_text="If the site can accomodate more than 35 4th graders.")

    best_visit_times = models.ManyToManyField(BestVisitTime)
    facilities = models.ManyToManyField(YouthFacility)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.agency + self.name)[:50]
        super(FieldTripSite, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'agency')


class FederalSite(models.Model):
    """ These sites are those you can get some form of an annual interagency
    pass at. """

    # The various sites are identified by either what kind they are,
    # or which agency they are managed by.

    SITE_CHOICES = (
        ('NPS', 'National Park Service'),
        ('NWR', 'National Wildlife Refuge'),
        ('BLM', 'Bureau of Land Management'),
        ('NF', 'National Forest'),
        ('NRA', 'National Recreation Area'),
        ('NHS', 'National Historic Site'),
        ('OTH', 'Other')
    )

    name = models.CharField(max_length=256)
    site_type = models.CharField(max_length=3, choices=SITE_CHOICES)
    phone = PhoneNumberField(null=True)
    phone_extension = models.IntegerField(null=True)
    city = models.CharField(max_length=128)
    state = USStateField(blank=False, null=False)
    website = models.URLField(max_length=512)
    slug = models.SlugField(unique=True, null=True)
    annual_pass = models.BooleanField(
        default=False, help_text="True if the site offers an annual pass")
    senior_pass = models.BooleanField(
        default=False, help_text="True if the site offers a senior pass")
    access_pass = models.BooleanField(
        default=False, help_text="True if the site offers an access pass")

    def __str__(self):
        return "%s (%s, %s)" % (self.name, self.city, self.state)

    class Meta:
        unique_together = ('name', 'city')
