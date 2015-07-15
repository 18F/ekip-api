from django.shortcuts import render

from .forms import PassSiteStateForm
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


def educator_passes(request):
    return render(
        request,
        'get-your-pass/educator_passes.html',
        {}
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

