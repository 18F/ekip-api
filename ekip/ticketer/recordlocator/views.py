from django.conf.urls import url

from recordlocator import generator
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.resources import skip_prepare

from .models import Ticket


# The maximum number of record locators that can be requested
MAX_REQUESTABLE = 50


class TicketResource(DjangoResource):

    def __init__(self, *args, **kwargs):
        super(TicketResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'issue': {
                'GET': 'issue',
            }
        })

        self.ticket_preparer = FieldsPreparer(fields={
            'record_locator': 'record_locator'
        })

    def prepare_tickets(self, tickets):
        locators = []
        for t in tickets:
            locators.append(self.ticket_preparer.prepare(t))

        data = {
            'locators': locators
        }
        return data


    @skip_prepare
    def issue(self, num_locators=1, zip_code=None):
        if self.request and 'num_locators' in self.request.GET:
            num_locators = self.request.GET.get('num_locators', 1)
            num_locators = int(num_locators)

        if self.request and 'zip' in self.request.GET:
            zip_code = self.request.GET.get('zip', '00000')

        tickets, _ = create_tickets(zip_code, num_locators)
        response = self.prepare_tickets(tickets)
        return response

    # Finally, extend the URLs
    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(TicketResource, cls).urls(name_prefix=name_prefix)
        new = [
            url(
                r'^issue/', cls.as_view('issue'),
                name=cls.build_url_name('issue', name_prefix)),
        ] + urlpatterns
        print(new)
        return new


def locator_exists(locator):
    """ Return True if this locator already exists in the Ticket database. """
    return Ticket.objects.filter(record_locator=locator).exists()


def create_unique_ticket(zip_code):
    """ This will attempt to create a unique Ticket (as identified by record
    locator). It tries a couple times, before using a separate scheme for
    Ticket generation. If that fails, this currently fails. We might later want
    to explore modes where this never fails. """

    locator = generator.safe_generate()
    ticket = None

    if not locator_exists(locator):
        ticket = create_new_ticket(zip_code, locator)
    else:
        # Locator is already used, generate another one.
        locator = generator.safe_generate()
        if not locator_exists(locator):
            ticket = create_new_ticket(zip_code, locator)
        else:
            # Second locator is also used, generate a completely different
            # type.
            locator = generate_backup_locator()
            if not locator_exists(locator):
                ticket = create_new_ticket(zip_code, locator)
            else:
                # Trying infinitely doesn't make sense. Fail.
                locator = None
                ticket = None
    return ticket


def create_tickets(zip_code, num_locators=1):
    """ Create tickets, ensuring that the associated record locators are
    unique. Return the list of those locators corresponding to new tickets. """

    tickets = []
    failures = []

    for r in range(0, num_locators):
        ticket = create_unique_ticket(zip_code)
        if ticket:
            tickets.append(ticket)
        else:
            failures.append(1)
    return tickets, failures


def create_new_ticket(zip_code, locator):
    """ Create and save a ticket. """

    ticket = Ticket(zip_code=zip_code, record_locator=locator)
    ticket.save()
    return ticket


def generate_backup_locator():
    """ This generates a 16 character locator when we keep generating
    duplicates. """
    return generator.timestamp_generate()
