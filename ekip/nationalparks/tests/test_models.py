from django.test import TestCase

from ..models import FederalSite

class FederalSiteTest(TestCase):
    def test_kids_pass(self):
        fs = FederalSite(
            name='Site',
            site_type='NPS',
            phone='301-425-5555',
            city='Anytown',
            state='MD',
            annual_pass=True,
            active_participant=True,
            version=0
        )
        fs.save()
        self.assertTrue(fs.kids_pass)

        fs.annual_pass = False
        fs.save()
        self.assertFalse(fs.kids_pass)

        fs.annual_pass = True
        fs.active_participant = False
        self.assertFalse(fs.kids_pass)
