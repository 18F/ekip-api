import csv
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.db.models import Sum
from django.template import defaultfilters

from localflavor.us.us_states import US_STATES

from .forms import FederalSiteStateForm, VoucherEntryForm
from nationalparks.api import FederalSiteResource
from ticketer.recordlocator.models import Ticket, AdditionalRedemption
from nationalparks.models import FederalSite
from everykid.models import Educator


class States():
    """ Create a map of two-letter state codes and the state name. """
    def __init__(self):
        self.states = {}
        for abbr, name in US_STATES:
            self.states[abbr] = name


def get_num_tickets_exchanged():
    """ Get a count of how many unique paper passes have been exchanged for plastic
    passes."""

    return Ticket.objects.filter(recreation_site__isnull=False).count()


def get_num_tickets_exchanged_more_than_once():
    """ Sum up all the additional redemptions for tickets. """
    return AdditionalRedemption.objects.count()


def convert_to_date(s):
    """ Convert the date into a useful format. """
    return datetime.strptime(s, '%Y%m%d')


@permission_required('recordlocator.view_exchange_data')
def csv_redemption(request):
    """ The redemption master data. """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exchanges.csv"'

    start_date = request.GET.get('start', '20150901')
    start_date = convert_to_date(start_date)
    end_date = request.GET.get('end', None)

    exchanged_tickets = Ticket.objects.filter(recreation_site__isnull=False)
    exchanged_tickets = exchanged_tickets.filter(
        redemption_entry__gte=start_date)
    if end_date:
        end_date = datetime.strptime(end_date, '%Y%m%d')
        exchanged_tickets = exchanged_tickets.filter(
            redemption_entry__lte=end_date)
    exchanged_tickets = exchanged_tickets.select_related('recreation_site')
    exchanged_tickets = exchanged_tickets.prefetch_related('additionalredemption_set')

    writer = csv.writer(response)

    # Write the headers
    writer.writerow([
        'pass_record_locator',
        'created',
        'recorded', 
        'zip', 
        'location', 
        'city',
        'state',
        'duplicate',
    ])

    DATE_FORMAT = 'Ymd'
    for ticket in exchanged_tickets:

        duplicates_exist = ticket.additionalredemption_set.count() > 0
        writer.writerow([
            ticket.record_locator,
            defaultfilters.date(ticket.created, DATE_FORMAT),
            defaultfilters.date(ticket.redemption_entry, DATE_FORMAT),
            ticket.zip_code,
            ticket.recreation_site.name,
            ticket.recreation_site.city,
            ticket.recreation_site.state,
            duplicates_exist
        ])

        for ar in ticket.additionalredemption_set.all():
            writer.writerow([
                ticket.record_locator,
                defaultfilters.date(ticket.created, DATE_FORMAT),
                defaultfilters.date(ar.redemption_entry, DATE_FORMAT),
                ticket.zip_code,
                ar.recreation_site.name,
                ar.recreation_site.city, 
                ar.recreation_site.state,
                duplicates_exist
            ])
    return response


@permission_required('recordlocator.view_exchange_data')
def tables(request):
    """ Give certain user a deeper look into the data. """

    return render(
        request,
        'data-index.html',
        {}
    )


@login_required
def statistics(request):
    educator_tickets = Educator.objects.all().aggregate(
        Sum('num_students'))['num_students__sum']

    unique_exchanges = get_num_tickets_exchanged()
    additional_exchanges = get_num_tickets_exchanged_more_than_once()

    return render(
        request,
        'stats.html',
        {
            'num_tickets_issued': Ticket.objects.count(),
            'num_tickets_exchanged': unique_exchanges,
            'all_exchanged': unique_exchanges + additional_exchanges,
            'educator_tickets_issued': educator_tickets
        }
    )


@login_required
def sites_for_state(request):
    """ Display a list of FederalSites per state. """

    state = request.GET.get('state')
    sites = FederalSiteResource().list(state)
    states_lookup = States()
    return render(
        request,
        'redemption-list-state.html',
        {
            'sites': sites,
            'state_name': states_lookup.states[state]
        }
    )


@login_required
def get_passes_state(request):
    """ Display a state selector, so that we can display the list of pass
    issuing federal sites by state. """

    if request.method == "POST":
        form = FederalSiteStateForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            return HttpResponseRedirect('/redeem/sites/?state=%s' % state)
    else:
        form = FederalSiteStateForm()
    return render(request, 'redemption-state.html', {'form': form})


def redeem_voucher(voucher_id, federal_site):
    """ If the Ticket exists and is not redeemed, redeem it at federal_site.
    """

    try:
        ticket = Ticket.objects.get(record_locator=voucher_id)

        if ticket.redemption_entry is None:
            ticket.redeem(federal_site)
        else:
            # This ticket has been redeemed before
            ar = AdditionalRedemption(
                ticket=ticket, recreation_site=federal_site)
            ar.save()

    except Ticket.DoesNotExist:
        ticket = None
    return ticket


def redeem_vouchers(formset, federal_site):
    """ Redeem all the vouchers that come through on the formset. """

    for form in formset:
        if form.has_changed():
            voucher_id = form.cleaned_data['voucher_id']
            redeem_voucher(voucher_id, federal_site)


@login_required
def redeem_confirm(request, slug):
    """ After a voucher ID form has been submitted, display a confirmation of
    success. """
    federal_site = get_object_or_404(FederalSite, slug=slug)

    return render(
        request,
        'redeem-confirm.html',
        {'pass_site': federal_site})


@login_required
def redeem_for_site(request, slug):
    """ Display and process a form that allows a user to enter multiple voucher
    ids for a single recreation site. """

    federal_site = get_object_or_404(FederalSite, slug=slug)
    VoucherEntryFormSet = formset_factory(VoucherEntryForm, extra=10)

    if request.method == "POST":
        formset = VoucherEntryFormSet(request.POST)
        if formset.is_valid():
            redeem_vouchers(formset, federal_site)
            return HttpResponseRedirect('/redeem/done/%s/' % slug)
    else:
        formset = VoucherEntryFormSet()

    return render(
        request,
        'voucher-entry.html',
        {
            'formset': formset,
            'pass_site': federal_site
        })
