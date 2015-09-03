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
STATES['PR'] = 'Puerto Rico'
STATES['VI'] = 'Virgin Islands'

def planyourtrip(request):
    """ We launched with /planyoutrip printed on the vouchers.  Make that URL
    work. """

    return HttpResponseRedirect(reverse('plan_your_trip'))


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

    if 'game_end' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    request.session['game_success'] = True
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
            request.session['ok_to_start'] = True
            return HttpResponseRedirect(reverse('adventure_start'))
    else:
        form = FourthGraderForm()
    return render(
        request,
        'get-your-pass/student_pass.html',
        {'form': form}
    )


def get_active_pass_exchange_sites(state):
    """ For a given state, return the sites that are issuing kids passes. """

    all_sites = FederalSiteResource().list(state)
    sites = [s for s in all_sites if s.kids_pass]
    return sites

def pass_exchange(request):
    """Display the list of sites one can exchange a voucher for a pass at."""

    state = request.GET.get('state')

    if state:
        sites = get_active_pass_exchange_sites(state)
        form = PassSiteStateForm(initial={'state': state})
        state_name = STATES[state]
    else:
        form = PassSiteStateForm()
        sites = []
        state_name = None

    return render(
        request,
        'plan-your-trip/pass_exchange.html',
        {
            'sites': sites,
            'form': form,
            'state_name': state_name
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


def create_educator(data):
    """ Given a dictionary with all the right fields, create an Educator
    object.  """

    educator = Educator(
        name=data['name'],
        work_email=data['work_email'],
        organization_name=data['organization_name'],
        org_or_school=data['org_or_school'],
        address_line_1=data['address_line_1'],
        address_line_2=data['address_line_2'],
        city=data['city'],
        state=data['state'],
        zipcode=data['zipcode'],
        num_students=data['num_students']
    )
    educator.save()
    return educator


class EducatorFormPreview(FormPreview):
    """ The educator contact information form requires a preview screen. This
    class manages that preview process. """

    form_template = 'get-your-pass/educator_passes.html'
    preview_template = 'get-your-pass/educator_passes_preview.html'

    def done(self, request, cleaned_data):
        educator = create_educator(cleaned_data)
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
    if 'game_success' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    zip_code = request.GET.get('zip', '00000')
    locator = issue_single_voucher(zip_code)

    return render(
        request,
        'get-your-pass/fourth_grade_voucher.html',
        {'locator': locator}
    )
