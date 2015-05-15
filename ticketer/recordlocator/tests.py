import json

from django.test import TestCase
from django.test import Client

from .views import generate_locators


class GeneratorTests(TestCase):
    """ Tests the generation of unique record locators """

    def test_generate_locators(self):
        """ Ensure that a single locator is generated, with no parameters. """
        locators = generate_locators()
        self.assertEqual(len(locators), 1)
        self.assertEqual(len(locators[0]), 8)

    def test_multiple_locators(self):
        """ Test that multiple locators are generated, and are unique. """
        locators = generate_locators(n=10)
        self.assertEqual(len(locators), 10)
        self.assertEqual(len(set(locators)), 10)


class RecordLocatorAPITests(TestCase):
    """ Tests for the RecordLocator API. """

    def test_api_generate_locators(self):
        c = Client()
        response = c.get('/locator/locator/')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('record_locators' in r)
        self.assertEqual(len(r['record_locators']), 1)

    def test_api_multiple_locators(self):
        c = Client()
        response = c.get('/locator/locator/?n=50')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode('utf8'))
        self.assertTrue('record_locators' in r)
        self.assertEqual(len(r['record_locators']), 50)

    def test_maximum_record_locators(self):
        c = Client()
        response = c.get('/locator/locator/?n=100')
        self.assertEqual(400, response.status_code)
