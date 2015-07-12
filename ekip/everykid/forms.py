from django import forms
from localflavor.us.us_states import US_STATES


# The U.S. states including DC and Puerto Rico
STATES_AND_PR = US_STATES + (('PR', 'Puerto Rico'), )
STATES_AND_PR = sorted(STATES_AND_PR, key=lambda x: x[1])


class StateSelect(forms.Select):
    """ A Select widget that uses a list of U.S. states including Puerto Rico.
    It excludes most other territories.  """

    def __init__(self, attrs=None):
        super(StateSelect, self).__init__(attrs, choices=STATES_AND_PR)


class PassSiteStateForm(forms.Form):
    state = forms.CharField(label="State", widget=StateSelect())