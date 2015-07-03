from django import forms

from localflavor.us.forms import USStateSelect
from recordlocator.generator import SAFE_ALPHABET


class FederalSiteStateForm(forms.Form):
    state = forms.CharField(label="State",  widget=USStateSelect())


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
