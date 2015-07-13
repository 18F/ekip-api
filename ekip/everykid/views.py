from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import PassSiteStateForm, EducatorForm
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
        'pass_exchange.html',
        {
            'sites': sites,
            'form': form
        }
    )

def educator_vouchers(request):
    num_vouchers = request.GET.get('num_vouchers', 1)

    return render(
        request,
        'educator_vouchers.html',
        {
            'num_vouchers': num_vouchers
        }
    )


def educator_passes(request):
    if request.method == 'POST':
        form = EducatorForm(request.POST)
        if form.is_valid():
            educator = form.save()
            return HttpResponseRedirect(
                '/get-your-pass/educator/vouchers/?num_vouchers=10')
    else:
        form = EducatorForm()
    return render(
        request,
        'educator_passes.html',
        {'form': form}
    )


def learn(request):
    return render(
        request,
        'learn.html',
        {}
    )
