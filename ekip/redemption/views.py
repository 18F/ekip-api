import csv
import json
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.db.models import Sum, Count
from django.template import defaultfilters

from localflavor.us.us_states import US_STATES, US_TERRITORIES

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
        for abbr, name in US_TERRITORIES:
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
    return datetime.strptime(s, '%m/%d/%Y')

def convert_to_db_date(s):
    """ Convert the date into a useful format. """
    date = convert_to_date(s)
    return date.strftime('%Y-%m-%d')

def get_tickets_by_states(start_date, end_date):

    # Base query with a date range.
    ticket_date_query = Ticket.objects \
               .extra(select={'day': "to_char(created, 'MMDDYYYY')"}) \
               .filter(created__range=(convert_to_db_date(start_date), convert_to_db_date(end_date)))

    # Get all Tickets created, grouped by State.
    tickets_by_state = ticket_date_query \
               .values('recreation_site__state') \
               .annotate(count=Count('created'))

    tickets_states = []
    if tickets_by_state:
        for ticket in tickets_by_state:
            tickets_states.append({'state':ticket['recreation_site__state'], 'count':ticket['count']})

    tickets_states = json.dumps(tickets_states)
    return tickets_states

def get_tickets_by_dates(start_date, end_date):

    # Base query with a date range.
    ticket_date_query = Ticket.objects \
                .extra(select={
                        'month': "EXTRACT(month FROM created)",
                        'year': "EXTRACT(year FROM created)"
                }) \
                .filter(created__range=(convert_to_db_date(start_date), convert_to_db_date(end_date)))

    # Get all Tickets created, grouped by date.
    tickets_by_date = ticket_date_query \
               .values('month','year') \
               .annotate(count=Count('created'))

    tickets_dates = []
    if tickets_by_date:
        for ticket in tickets_by_date:
            tickets_dates.append({'date': str(int(ticket['year'])) + str(int(ticket['month'])), 'count':ticket['count']})

    tickets_dates = json.dumps(tickets_dates)
    return tickets_dates

def refresh_stats(request):

    if request.method == 'GET':
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        response_data = {
            'tickets_by_states': get_tickets_by_states(start_date,end_date),
            'tickets_by_dates': get_tickets_by_dates(start_date,end_date)
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@permission_required('recordlocator.view_exchange_data')
def csv_redemption(request):
    """ The redemption master data. """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exchanges.csv"'

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date is None:
        # Default date = Start of year.
        start_date = datetime(datetime.now().year, 1, 1)
    else:
        start_date = convert_to_date(start_date)

    exchanged_tickets = Ticket.objects.filter(recreation_site__isnull=False)
    exchanged_tickets = exchanged_tickets.filter(
        redemption_entry__gte=start_date)
    if end_date:
        end_date = convert_to_date(end_date)
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

    if not educator_tickets:
        educator_tickets = 0

    unique_exchanges = get_num_tickets_exchanged()
    additional_exchanges = get_num_tickets_exchanged_more_than_once()
    num_tickets_issued = Ticket.objects.count()

    one_year_ago = (datetime.now() - timedelta(days=1*365)).strftime('%m/%d/%Y')
    today = datetime.now().strftime('%m/%d/%Y')

    return render(
        request,
        'stats.html',
        {
            'start_date': one_year_ago,
            'end_date': today,
            'tickets_dates': get_tickets_by_dates(one_year_ago, today),
            'tickets_states': get_tickets_by_states(one_year_ago, today),
            'num_tickets_issued': num_tickets_issued,
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
