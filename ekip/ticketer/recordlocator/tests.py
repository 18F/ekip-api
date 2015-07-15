import json
from unittest import mock

from django.test import TestCase
from django.test import Client

from ticketer.recordlocator import views
from .models import Ticket


def mock_generator(length=1):
    """ A mock record locator generator that returns the same record locator
    each time. """

    return 'XXXXXXXX'


class TicketCreationTests(TestCase):
    def test_create_new_ticket(self):
        """ Test the creation of a new ticket. """
        views.create_new_ticket(20852, 'XXYZZYCD')
        ticket = Ticket.objects.filter(record_locator='XXYZZYCD')[0]
        self.assertEqual(ticket.zip_code, '20852')

    def test_generate_backup_locator(self):
        locator = views.generate_backup_locator()
        self.assertTrue('-' in locator)
        self.assertEqual(16, len(locator))

    def test_create_tickets(self):
        tickets, failures = views.create_tickets(20852, 5)
        self.assertEqual(5, len(tickets) + len(failures))

        # Failures should be extremely rare
        self.assertTrue(len(tickets) > 0)

        locators = [t.record_locator for t in tickets]

        # Locators are unique with respect to each other.
        self.assertEqual(len(locators), len(set(locators)))

        for l in locators:
            ticket = Ticket.objects.get(record_locator=l)
            self.assertNotEqual(None, ticket)
            self.assertEqual(ticket.zip_code, '20852')

    @mock.patch(
        'ticketer.recordlocator.views.generator.safe_generate', mock_generator)
    def test_create_unique_ticket(self):
        ticket_one = views.create_unique_ticket(16801)
        self.assertEqual(ticket_one.record_locator, 'XXXXXXXX')

        ticket_two = views.create_unique_ticket(16801)
        self.assertTrue('-' in ticket_two.record_locator)
        self.assertTrue('XXXXXXXX' in ticket_two.record_locator)

        ticket_three = views.create_unique_ticket(20002)
        self.assertTrue('-' in ticket_three.record_locator)
        self.assertTrue('XXXXXXXX' in ticket_three.record_locator)

        self.assertNotEqual(
            ticket_two.record_locator, ticket_three.record_locator)


class RecordLocatorAPITests(TestCase):
    """ Tests for the RecordLocator API. """

    def test_api_generate_locators(self):
        c = Client()
        response = c.get('/api/tickets/issue/?zip=20852')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('locators' in r)
        self.assertEqual(len(r['locators']), 1)

    def test_api_multiple_locators(self):
        c = Client()
        response = c.get('/api/tickets/issue/?zip=20852&num_locators=50')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('locators' in r)
        self.assertEqual(len(r['locators']), 50)


class TicketGeneratorTest(TestCase):
    """ Tests for the RecordLocator API. """

    def test_ticket_zip_match(self):
        c = Client()
        response = c.get('/api/tickets/issue/?zip=91381')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertEqual(
            '91381',
            Ticket.objects.get(
                record_locator=r['locators'][0]['record_locator']).zip_code)
