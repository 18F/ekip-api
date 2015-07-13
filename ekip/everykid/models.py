from django.db import models
from localflavor.us.models import USStateField, USZipCodeField

class Educator(models.Model):
    """ An educator has to fill out this form before they can download vouchers
    for their students. """

    name = models.CharField(max_length=128)
    work_email = models.CharField(max_length=128, null=True)
    organization_name = models.CharField(max_length=128)
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = USStateField(blank=False, null=False)
    zipcode = USZipCodeField()
