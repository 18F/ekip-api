from django import forms
from django.utils.translation import ugettext_lazy as _

from localflavor.us.us_states import US_STATES
from localflavor.us.forms import USZipCodeField

from .models import Educator


# The U.S. states including DC and Puerto Rico
STATES_AND_PR = US_STATES + (('PR', 'Puerto Rico'), )
STATES_AND_PR = sorted(STATES_AND_PR, key=lambda x: x[1])


class StateSelect(forms.Select):
    """ A Select widget that uses a list of U.S. states including Puerto Rico.
    It excludes most other territories.  """

    def __init__(self, attrs=None):
        super(StateSelect, self).__init__(attrs, choices=STATES_AND_PR)


class PassSiteStateForm(forms.Form):
    state = forms.CharField(label=_("State"), widget=StateSelect())


class EducatorForm(forms.ModelForm):
    org_or_school = forms.ChoiceField(
        label=_("School or qualified organization"), widget=forms.RadioSelect,
        choices=Educator.ORG_CHOICES)

    class Meta:
        model = Educator
        fields = [
            'name', 'work_email', 'org_or_school', 'organization_name', 'address_line_1',
            'address_line_2', 'city', 'state', 'zipcode', 'num_students']


class FourthGraderForm(forms.Form):
    """
        A very simple, one field form that is used to confirm whether the
        student is a 4th grader.
    """

    STUDENT_CHOICES = (
        ('Y', _('Yes, I am in the 4th grader (or 10 years old)')),
        ('N', _('No')))

    in_the_fourth_grade = forms.ChoiceField(
        label=_("Are you a 4th grader?"),
        widget=forms.RadioSelect,
        choices=STUDENT_CHOICES)


class ZipCodeForm(forms.Form):
    """
        This is the form that allows us to ask 4th graders for their ZIP code.
    """

    zip_code = USZipCodeField(label=_("What is your ZIP code?"))
