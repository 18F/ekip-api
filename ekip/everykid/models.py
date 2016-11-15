from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from localflavor.us.models import USStateField, USZipCodeField


class Educator(models.Model):
    """ An educator has to fill out this form before they can download vouchers
    for their students. """

    ORG_CHOICES = (('S', _('School')), ('O', _('Qualified organization')))


    name = models.CharField(_("Educator's full name"), max_length=128)
    work_email = models.CharField(
        _("Work email address"), max_length=128, null=True)
    organization_name = models.CharField(
        _("School or organization name"), max_length=128)
    org_or_school = models.CharField(_(""), max_length=1, choices=ORG_CHOICES)
    address_line_1 = models.CharField(
        _("Address line 1"), max_length=128)
    address_line_2 = models.CharField(
        _("Address line 2"), max_length=128, null=True, blank=True)
    city = models.CharField(_("City"), max_length=50)
    state = USStateField(_("State"), blank=False, null=False)
    zipcode = USZipCodeField(_("Zip"))
    num_students = models.IntegerField(
        _("Number of students"),
        validators=[
            MaxValueValidator(
                50, _('You can only print up to 50 passes at a time.')),
            MinValueValidator(1, _('You can not print less than one pass.'))],
        help_text="Number of students for which you are requesting vouchers")
