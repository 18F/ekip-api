from django import forms

from localflavor.us.us_states import US_STATES
from recordlocator.generator import SAFE_ALPHABET

# The U.S. states including DC and Puerto Rico
STATES_AND_PR = US_STATES + (('PR', 'Puerto Rico'), ('VI', 'Virgin Islands'))
STATES_AND_PR = sorted(STATES_AND_PR, key=lambda x: x[1])

class StateSelect(forms.Select):
    """ A Select widget that uses a list of U.S. states including Puerto Rico.
    It excludes most other territories.  """

    def __init__(self, attrs=None):
        super(StateSelect, self).__init__(attrs, choices=STATES_AND_PR)


class FederalSiteStateForm(forms.Form):
    state = forms.CharField(label="State",  widget=StateSelect())


class VoucherEntryForm(forms.Form):
    voucher_id = forms.CharField(label='Voucher ID', max_length=25)

    def clean_voucher_id(self):
        voucher_id = self.cleaned_data['voucher_id']
        voucher_id = voucher_id.strip().upper()

        if len(voucher_id) > 16:
            raise forms.ValidationError('ID is too long')
        elif len(voucher_id) < 8:
            raise forms.ValidationError('ID is too short')

        candidate = voucher_id
        if '-' in voucher_id:
            candidate = voucher_id.split()

        for c in candidate:
            if c not in SAFE_ALPHABET:
                raise forms.ValidationError('Unexpected character in ID')

        return voucher_id
