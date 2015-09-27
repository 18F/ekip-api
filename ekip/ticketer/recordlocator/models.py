from django.db import models
from django.utils import timezone

from localflavor.us.models import USZipCodeField
from nationalparks.models import FederalSite


class Ticket(models.Model):
    """ This is a voucher. """

    zip_code = USZipCodeField(max_length=5)
    record_locator = models.CharField(max_length=16, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    recreation_site = models.ForeignKey(FederalSite, null=True)
    redemption_entry = models.DateTimeField(null=True)

    def redeem(self, federal_site):
        self.recreation_site = federal_site
        self.redemption_entry = timezone.now()
        self.save()

    def __str__(self):
        return "%s %s" % (self.record_locator, self.zip_code)

    class Meta:
        permissions = (('view_exchange_data', 'Can view exchange data'),)

class AdditionalRedemption(models.Model):
    """ Create this, when a ticket is redeemed more than once. """

    ticket = models.ForeignKey(Ticket)
    recreation_site = models.ForeignKey(FederalSite, null=False)
    redemption_entry = models.DateTimeField(auto_now_add=True)
