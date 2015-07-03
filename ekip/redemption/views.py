from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

from localflavor.us.us_states import US_STATES

from .forms import FederalSiteStateForm, VoucherEntryForm
from nationalparks.api import FederalSiteResource
from nationalparks.models import FederalSite

class States():
    def __init__(self):
        self.states = {}
        for abbr, name in US_STATES:
            self.states[abbr] = name


def sites_for_state(request):
    state = request.GET.get('state', None)
    sites = FederalSiteResource().list(state)
    states_lookup = States()
    return render(
        request, 
        'redemption-list-state.html',
        {'sites': sites, 
        'state_name': states_lookup.states[state]}
    )
    

def get_passes_state(request):
    if request.method == "POST":
        form = FederalSiteStateForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            return HttpResponseRedirect('/redeem/sites/?state=%s' % state)
    else:
        form = FederalSiteStateForm()
    return render(request, 'redemption-state.html', {'form': form})


def process_voucher_id(voucher_id):
    pass

def process_voucher_ids(formset):
    for form in formset:
        if form.has_changed():
            voucher_id = form.cleaned_data['voucher_id']
            process_voucher_id(voucher_id)



def redeem_for_site(request, slug):
    federal_site = get_object_or_404(FederalSite, slug=slug)
    VoucherEntryFormSet = formset_factory(VoucherEntryForm, extra=6)

    if request.method == "POST":
        formset = VoucherEntryFormSet(request.POST)
        if formset.is_valid():
            process_voucher_ids(formset)
            return HttpResponseRedirect('/redeem/')
    else:
        formset = VoucherEntryFormSet()

    return render(
        request,
        'voucher-entry.html',
        {
            'formset': formset, 
            'pass_site': federal_site
        })
