from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
from .views import redeem_voucher
from nationalparks.models import FederalSite


class RedemptionTestCase(TestCase):
    fixtures = ['federalsites.json', 'tickets.json']

    def test_redeem_voucher(self):
        """ Test the redemption of a voucher here. """
        federal_site = FederalSite.objects.get(
            slug="nf-talladega-talladega-ranger")
        ticket = redeem_voucher('6PZDJ7TP', federal_site)
        self.assertEqual(ticket.record_locator, '6PZDJ7TP')


class SitesTestCase(TestCase):
    fixtures = ['federalsites.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'john@doi.gov', 'password')

    def test_behind_password(self):
        response = self.client.get('/redeem/sites/', {'state': 'AZ'})
        self.assertRedirects(
            response, '/accounts/login/?next=/redeem/sites/%3Fstate%3DAZ')
        
    def test_sites_for_state(self):
        """ We display FederalSites by state. Test that display here. """
        self.client.login(username='john', password='password')
        response = self.client.get('/redeem/sites/', {'state': 'AZ'})
        self.assertEqual(200, response.status_code)

        content = response.content.decode('utf-8')

        self.assertTrue('Rainbow Bridge' in content)
        self.assertTrue('Aqua Fria' in content)
