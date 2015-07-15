from django.shortcuts import render
from django.http import HttpResponseRedirect

from formtools.preview import FormPreview

from .forms import PassSiteStateForm
from .models import Educator
from ticketer.recordlocator.views import TicketResource
from nationalparks.api import FederalSiteResource


def plan_your_trip(request):
    return render(
        request,
        'plan-your-trip/index.html',
        {}
    )


def student_pass(request):
    return render(
        request,
        'get-your-pass/student_pass.html',
        {}
    )


def pass_exchange(request):
    """ Display the list of sites one can exchange a voucher for a pass at. """

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


def learn(request):
    return render(
        request,
        'learn/index.html',
        {}
    )


def fourth_grade_voucher(request):
    return render(
        request,
        'get-your-pass/fourth_grade_voucher.html',
        {}
    )

