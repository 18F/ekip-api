import json

from django.test import TestCase
from django.test import Client

from .views import create_new_ticket, generate_backup_locator, create_tickets
from .models import Ticket

class TicketCreationTests(TestCase):
    def test_create_new_ticket(self):
        """ Test the creation of a new ticket. """
        create_new_ticket(20852, 'XXYZZYCD')
        ticket = Ticket.objects.filter(record_locator='XXYZZYCD')[0]
        self.assertEqual(ticket.zip_code, '20852')

    def test_generate_backup_locator(self):
        locator = generate_backup_locator()
        self.assertTrue('-' in locator)
        self.assertEqual(16, len(locator))

    def test_create_tickets(self):
        locators, failures = create_tickets(20852, 5)
        self.assertEqual(5, len(locators) + len(failures))

        #Failures should be extremely rare
        self.assertTrue(len(locators) > 0)

        #Locators are unique with respect to each other. 
        self.assertEqual(len(locators), len(set(locators)))

        for l in locators:
            ticket = Ticket.objects.get(record_locator=l)
            self.assertNotEqual(None, ticket)
            self.assertEqual(ticket.zip_code, '20852')


class RecordLocatorAPITests(TestCase):
    """ Tests for the RecordLocator API. """

    def test_api_generate_locators(self):
        c = Client()
        response = c.get('/ticket/')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('record_locators' in r)
        self.assertEqual(len(r['record_locators']), 1)

    def test_api_multiple_locators(self):
        c = Client()
        response = c.get('/ticket/?n=50')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('record_locators' in r)
        self.assertEqual(len(r['record_locators']), 50)

    def test_maximum_record_locators(self):
        c = Client()
        response = c.get('/ticket/?n=100')
        self.assertEqual(400, response.status_code)

class TicketGeneratorTest(TestCase):
    """ Tests for the RecordLocator API. """

    def test_ticket_zip_match(self):
        c = Client()
        response = c.get('/ticket/?zip=91381')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertEqual('91381', Ticket.objects.get(record_locator=r['record_locators'][0]).zip_code)
