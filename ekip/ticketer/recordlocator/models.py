from django.db import models

from localflavor.us.models import USZipCodeField

# Create your models here.
class RedemptionLocation(models.Model):
    name = models.CharField(max_length=255)


class Ticket(models.Model):
    """ This is a ticket. """

    zip_code = USZipCodeField(max_length=5)
    record_locator = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    redeemed = models.ForeignKey(RedemptionLocation, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.record_locator, self.zip_code)
