from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
from .views import (
    redeem_voucher, get_num_tickets_exchanged,
    get_num_tickets_exchanged_more_than_once)
from nationalparks.models import FederalSite
from ticketer.recordlocator.models import AdditionalRedemption


class RedemptionTestCase(TestCase):
    fixtures = ['federalsites.json', 'tickets.json']

    def test_redeem_voucher(self):
        """ Test the redemption of a voucher here. """
        federal_site = FederalSite.objects.get(
            slug="nf-talladega-talladega-ranger")
        ticket = redeem_voucher('6PZDJ7TP', federal_site)
        self.assertEqual(ticket.record_locator, '6PZDJ7TP')
        self.assertIsNotNone(ticket.redemption_entry, None)

    def test_multiple_redemptions(self):
        federal_site = FederalSite.objects.get(
            slug="nf-talladega-talladega-ranger")
        ticket = redeem_voucher('XZ6HGDXR', federal_site)

        self.assertEqual(ticket.record_locator, 'XZ6HGDXR')
        self.assertIsNotNone(ticket.redemption_entry, None)

        ticket = redeem_voucher('XZ6HGDXR', federal_site)

        ars = AdditionalRedemption.objects.filter(
            ticket__record_locator='XZ6HGDXR')
        self.assertEqual(len(ars), 1)
        self.assertEqual(ars[0].ticket.record_locator, 'XZ6HGDXR')


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


class StatisticsTestCase(TestCase):
    fixtures = ['federalsites.json', 'tickets.json']

    def test_paper_exchanged(self):
        """ When a paper pass has been exchanged, the statistic should report
        that """

        before = get_num_tickets_exchanged()

        federal_site = FederalSite.objects.get(
            slug="nf-talladega-talladega-ranger")
        ticket = redeem_voucher('6PZDJ7TP', federal_site)
        self.assertEqual(ticket.record_locator, '6PZDJ7TP')
        self.assertIsNotNone(ticket.redemption_entry, None)

        after = get_num_tickets_exchanged()

        self.assertTrue(after >= 1)
        self.assertTrue(after > before)

    def test_multiple_redemptions_statistics(self):

        before = get_num_tickets_exchanged_more_than_once()

        federal_site = FederalSite.objects.get(
            slug="nf-talladega-talladega-ranger")
        ticket = redeem_voucher('XZ6HGDXR', federal_site)

        self.assertEqual(ticket.record_locator, 'XZ6HGDXR')
        self.assertIsNotNone(ticket.redemption_entry, None)

        ticket = redeem_voucher('XZ6HGDXR', federal_site)

        ars = AdditionalRedemption.objects.filter(
            ticket__record_locator='XZ6HGDXR')
        self.assertEqual(len(ars), 1)
        self.assertEqual(ars[0].ticket.record_locator, 'XZ6HGDXR')

        after = get_num_tickets_exchanged_more_than_once()
        self.assertTrue(after > before)
