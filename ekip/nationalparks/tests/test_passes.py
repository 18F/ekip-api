from django.test import TestCase

from ..management.commands import passes as ps
from nationalparks.models import FederalSite

class PassesTests(TestCase):
    """ Tests for the redemption site list importer command """

    def test_process_site(self):
        row = {
            'name': 'Alaska BLM Office',
            'phone': '907-271-5960',
            'city': 'Anchorage',
            'state':'AK',
            'website': 'http://www.blm.gov/ak/st/en/fo/ado.html',
            'annual_senior': 'Yes',
            'access': 'Yes'
            }

        ps.process_site(row, 1)

        fs = FederalSite.objects.get(name='Alaska BLM Office')
        self.assertIsNotNone(fs)

        self.assertEqual('Alaska BLM Office', fs.name)
        self.assertEqual('907-271-5960', fs.phone)
        self.assertEqual('Anchorage', fs.city)
        self.assertEqual('AK', fs.state)
        self.assertEqual('http://www.blm.gov/ak/st/en/fo/ado.html', fs.website)
        self.assertEqual(True, fs.annual_pass)
        self.assertEqual(True, fs.senior_pass)
        self.assertEqual(True, fs.access_pass)

    def test_get_next_version(self):
        next_version = ps.get_next_version()
        self.assertIsNotNone(next_version)
        self.assertGreaterEqual(1, next_version)
