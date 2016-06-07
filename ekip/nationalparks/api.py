from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import FederalSite, FieldTripSite


class FederalSiteResource(DjangoResource):
    """ The API endpoint for FederalSites. """
    preparer = FieldsPreparer(fields={
        'name': 'name',
        'city': 'city'
    })

    def list(self, state=None, everykid=None):

        if self.request and 'state' in self.request.GET:
            state = self.request.GET.get('state')

        if self.request and 'everykid' in self.request.GET:
            # Only return those sites that issue the Every Kid in a Park pass
            everykid = True

        query = FederalSite.objects.all().order_by('name')

        if state:
            query = FederalSite.objects.filter(state=state)
        if everykid:
            query = query.filter(annual_pass=True, active_participant=True)

        return query


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
            return FieldTripSite.objects.filter(state=state).order_by('name')

        return FieldTripSite.objects.all().order_by('name')
