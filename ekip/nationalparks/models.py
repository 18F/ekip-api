from django.db import models

from localflavor.us.models import USStateField, PhoneNumberField


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

    class Meta:
        unique_together = ('name', 'city')
