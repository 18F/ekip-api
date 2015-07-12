from django.shortcuts import render

from nationalparks.models import FederalSite
from .forms import PassSiteStateForm
from nationalparks.api import FederalSiteResource


def plan_your_trip(request):
    return render(
        request,
        'plan_your_trip.html',
        {}
    )


def student_pass(request):
    return render(
        request,
        'student_pass.html',
        {}
    )


def pass_exchange_state(request, state):
    sites = FederalSite.objects.filter(state='MD')
    return render(
        request,
        'pass_exchange_state.html',
        {'sites': sites}
    )


def pass_exchange(request):
    state = request.GET.get('state', None)
    form = PassSiteStateForm()

    if state:
        sites = FederalSiteResource().list(state)
        form = PassSiteStateForm(initial={'state': state})
    else:
        sites = []

    return render(
        request,
        'pass_exchange.html',
        {
            'sites': sites,
            'form': form
        }
    )


def educator_passes(request):
    return render(
        request,
        'educator_passes.html',
        {}
    )


def learn(request):
    return render(
        request,
        'learn.html',
        {}
    )
