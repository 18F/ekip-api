from django.db import models

# Create your models here.
class RedemptionLocation(models.Model):
	name = models.CharField(max_length=255)


class Ticket(models.Model):
	zip_code = models.CharField(max_length=5)
	record_locator = models.CharField(max_length=8)
	created = models.DateTimeField(auto_now_add=True)
	redeemed = models.ForeignKey(RedemptionLocation, blank=True, null=True)