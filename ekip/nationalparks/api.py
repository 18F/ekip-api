from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import FederalSite, FieldTripSite


class FederalSiteResource(DjangoResource):
    """ The API endpoint for FederalSites. """
    preparer = FieldsPreparer(fields={
        'name': 'name',
        'city': 'city'
    })

    def list(self, state=None):

        if self.request and 'state' in self.request.GET:
            state = self.request.GET.get('state')

        if state:
            return FederalSite.objects.filter(state=state)

        return FederalSite.objects.all()


class FieldTripResource(DjangoResource):
    """ The API endpoint for FieldTripSites. """

    preparer = FieldsPreparer(fields={
        'name': 'name',
        'city': 'city',
        'website': 'website',
        'zipcode': 'zipcode',
        'advance_reservation': 'advance_reservation',
        'larger_groups': 'larger_groups'
    })

    def list(self, state=None):

        if self.request and 'state' in self.request.GET:
            state = self.request.GET.get('state', None)

        if state:
            return FieldTripSite.objects.filter(state=state)

        return FieldTripSite.objects.all()
