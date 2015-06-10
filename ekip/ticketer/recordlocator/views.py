import json

from django.http import HttpResponse, HttpResponseBadRequest

from recordlocator import generator

from .models import Ticket


# The maximum number of record locators that can be requested
MAX_REQUESTABLE = 50


def record_locators(request):
    """ View that generates at least one record locator, generating 'n' if
    specified through a query parameter. """

    num_locators = int(request.GET.get('n', 1))
    zip_code = request.GET.get('zip', '00000')

    if num_locators > MAX_REQUESTABLE:
        return HttpResponseBadRequest(
            'Maximum of %s record locators can be requested' % MAX_REQUESTABLE)

    record_locators = create_tickets(zip_code, num_locators)

    data = {'record_locators': record_locators}
    response = json.dumps(data)

    return HttpResponse(response, content_type='application/json')


def locator_exists(locator):
    """ Return True if this locator already exists in the Ticket database. """
    return Ticket.objects.filter(record_locator=locator).exists()


def create_unique_ticket(zip_code):
    """ This will attempt to create a unique Ticket (as identified by record
    locator). It tries a couple times, before using a separate scheme for
    Ticket generation. If that fails, this currently fails. We might later want
    to explore modes where this never fails. """

    locator = generator.safe_generate()
    if not locator_exists(locator):
        create_new_ticket(zip_code, locator)
    else:
        # Locator is already used, generate another one.
        locator = generator.safe_generate()
        if not locator_exists(locator):
            create_new_ticket(zip_code, locator)
        else:
            # Second locator is also used, generate a completely different
            # type.
            locator = generator.generate_backup_locator()
            if not locator_exists(locator):
                create_new_ticket(zip_code, locator)
            else:
                # Trying infinitely doesn't make sense. Fail.
                locator = None
    return locator


def create_tickets(zip_code, num_locators=1):
    """ Create tickets, ensuring that the associated record locators are
    unique. Return the list of those locators corresponding to new tickets. """

    locators = []
    failures = []

    for r in range(0, num_locators):
        locator = create_unique_ticket(zip_code)
        if locator:
            locators.append(locator)
        else:
            failures.append(locator)
    return locators


def create_new_ticket(zip_code, locator):
    """ Create and save a ticket. """

    ticket = Ticket(zip_code=zip_code, record_locator=locator)
    ticket.save()


def generate_backup_locator():
    """ This generates a 16 character locator when we keep generating
    duplicates. """
    return generator.timestamp_generate()

