from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from formtools.preview import FormPreview
from localflavor.us.us_states import US_STATES

from .forms import PassSiteStateForm, FourthGraderForm, ZipCodeForm
from .models import Educator
from ticketer.recordlocator.views import TicketResource
from nationalparks.api import FederalSiteResource, FieldTripResource
from nationalparks.models import FieldTripSite

STATES = {abbr: name for abbr, name in US_STATES}

def plan_your_trip(request):
    return render(
        request,
        'plan-your-trip/index.html',
        {}
    )


def game_success(request):
    """ This is the page that is displayed after the student succesfully
    completes the game. It'll collect the zipcode, and provide them with a link
    to the voucher. """

    if request.method == "POST":
        form = ZipCodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('%s?zip=%s' % (
                reverse('fourth_grade_voucher'),
                form.cleaned_data['zip_code']))
    else:
        form = ZipCodeForm()
    return render(
        request,
        'get-your-pass/game_success.html',
        {'form': form}
    )


def student_pass(request):
    """ This is the view where we ask if they are a 4th grader (and if they
    are) then forward them on to the first page of the game."""

    if request.method == "POST":
        form = FourthGraderForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('adventure_start'))
    else:
        form = FourthGraderForm()
    return render(
        request,
        'get-your-pass/student_pass.html',
        {'form': form}
    )


def pass_exchange(request):
    """Display the list of sites one can exchange a voucher for a pass at."""

    state = request.GET.get('state', None)

    if state:
        sites = FederalSiteResource().list(state)
        form = PassSiteStateForm(initial={'state': state})
    else:
        form = PassSiteStateForm()
        sites = []

    return render(
        request,
        'plan-your-trip/pass_exchange.html',
        {
            'sites': sites,
            'form': form
        }
    )


def field_trip_details(request, slug):
    destination = get_object_or_404(FieldTripSite, slug=slug)

    destination.visit_times_list = [
        v.best_time for v in destination.best_visit_times.all()]

    destination.features_list = [
        v.facility for v in destination.facilities.all()]

    return render(
        request, 
        'plan-your-trip/field_trip_details.html',
        {'destination': destination}
    )


def field_trip(request):
    """ Display the list of sites intended for field trips. """

    state = request.GET.get('state', None)
    state_name = None

    if state:
        sites = FieldTripResource().list(state)
        form = PassSiteStateForm(initial={'state': state})
        state_name = STATES[state]
    else:
        form = PassSiteStateForm()
        sites = []
    return render(
        request,
        'plan-your-trip/field_trip.html',
        {
            'sites': sites,
            'form': form,
            'state_name': state_name
        }
    )


class EducatorFormPreview(FormPreview):
    """ The educator contact information form requires a preview screen. This
    class manages that preview process. """

    form_template = 'get-your-pass/educator_passes.html'
    preview_template = 'get-your-pass/educator_passes_preview.html'

    def done(self, request, cleaned_data):
        educator = Educator(
            name=cleaned_data['name'],
            work_email=cleaned_data['work_email'],
            organization_name=cleaned_data['organization_name'],
            address_line_1=cleaned_data['address_line_1'],
            address_line_2=cleaned_data['address_line_2'],
            city=cleaned_data['city'],
            state=cleaned_data['state'],
            zipcode=cleaned_data['zipcode'],
            num_students=cleaned_data['num_students']
        )
        educator.save()
        return HttpResponseRedirect(
            'get-your-pass/educator/vouchers/?num_vouchers=%s&zip=%s' % (
                educator.num_students, educator.zipcode))


def educator_vouchers(request):
    num_vouchers = int(request.GET.get('num_vouchers', 1))
    zip_code = request.GET.get('zip', '00000')

    tickets = TicketResource().issue(num_vouchers, zip_code)
    locators = [t['record_locator'] for t in tickets.value['locators']]

    return render(
        request,
        'get-your-pass/educator_vouchers.html',
        {
            'num_vouchers': num_vouchers,
            'locators': locators,
        }
    )


def how_it_works(request):
    return render(
        request,
        'how-it-works/index.html',
        {}
    )


def issue_single_voucher(zip_code):
    """ Create a Ticket, and return a single record locator. """
    tickets = TicketResource().issue(1, zip_code)
    locators = [t['record_locator'] for t in tickets.value['locators']]
    return locators[0]


def fourth_grade_voucher(request):
    zip_code = request.GET.get('zip', '00000')
    locator = issue_single_voucher(zip_code)

    return render(
        request,
        'get-your-pass/fourth_grade_voucher.html',
        {'locator': locator}
    )
