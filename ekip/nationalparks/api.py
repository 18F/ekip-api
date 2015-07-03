from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import FederalSite


class FederalSiteResource(DjangoResource):
    """ The API endpoint for FederalSites. """
    preparer = FieldsPreparer(fields={
        'name': 'name',
        'city': 'city'
    })

    def list(self, state=None):

        if self.request and 'state' in self.request.GET:
            state = self.request.GET.get('state', 'None')

        if state:
            return FederalSite.objects.filter(state=state)

        return FederalSite.objects.all()
