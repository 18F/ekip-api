from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .views import (
    issue_single_voucher, STATES, create_educator,
    get_active_pass_exchange_sites)
from .models import Educator
from ticketer.recordlocator.models import Ticket


class BasicPageTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_get_pass(self):
        response = self.client.get(reverse('get_your_pass'))
        self.assertEquals(200, response.status_code)

    def test_get_fourth_grader_pass(self):
        response = self.client.get(reverse('student_pass'))
        self.assertEquals(200, response.status_code)

    def test_get_educator_passes(self):
        response = self.client.get(reverse('educator_passes'))
        self.assertEquals(200, response.status_code)

    def test_get_privacy_policy(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEquals(200, response.status_code)

    def test_field_trip(self):
        response = self.client.get(reverse('field_trip'))
        self.assertEquals(200, response.status_code)

    def test_planyoutrip(self):
        response = self.client.get(reverse('redirect_planner'))
        self.assertEquals(302, response.status_code)


class NavigationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_active_selector(self):
        response = self.client.get(reverse('how_it_works'))
        self.assertEquals(200, response.status_code)
        content = response.content.decode('utf-8')
        self.assertTrue('<li class="active">' in content)


class PassExchangeSiteTestCase(TestCase):
    fixtures = ['federalsites.json']

    def test_choose_by_state(self):
        c = Client()
        url = '%s?state=AZ' % reverse('pass_exchange')
        response = c.get(url)
        content = response.content.decode('utf-8')
        self.assertTrue('Aqua Fria National Monument' in content)
        self.assertTrue('Rainbow Bridge National Monument' in content)

    def test_states_mapping(self):
        self.assertEqual('Maryland', STATES['MD'])
        self.assertEqual('Colorado', STATES['CO'])
        self.assertEqual('Puerto Rico', STATES['PR'])
        self.assertEqual('Virgin Islands', STATES['VI'])

    def test_get_active_pass_exchange_sites(self):
        """ The fixture has an inactive site in California - so this should be
        empty. """

        sites = get_active_pass_exchange_sites('CA')
        self.assertTrue(len(sites) == 0)


class FourthGraderFlowTests(TestCase):

    def test_issue_single_voucher(self):
        locator = issue_single_voucher(20852)
        ticket = Ticket.objects.get(record_locator=locator)
        self.assertEqual('20852', ticket.zip_code)


class EducatorFormTests(TestCase):
    def test_educator_form(self):
        """ Check that certain form fields are required. """

        response = self.client.post(
            '/get-your-pass/educator/',
            {'work_email': 'abc@abc.gov', 'stage': '1'})

        required_fields = [
            'name', 'organization_name', 'address_line_1', 'city', 'state',
            'zipcode', 'num_students', 'org_or_school']

        for field in required_fields:
            self.assertFormError(
                response, 'form', field, 'This field is required.')

    def test_number_of_passes_limit(self):
        """ On the educator form, we can only request 50 passes at a time. Test
        that this is enforced. """

        response = self.client.post(
            '/get-your-pass/educator/',
            {
                'work_email': 'rj@teach.org',
                'stage': '1',
                'name': 'Rajiv Teacher',
                'organization_name': 'Zion Elementary',
                'address_line_1': '1 Main St.',
                'city': 'Austin',
                'state': 'TX',
                'zipcode': '78704',
                'num_students': '61',
                'org_or_school': 'S'
            })

        self.assertFormError(
            response, 'form', 'num_students',
            'You can only print up to 50 passes at a time.')

    def test_create_educator(self):
        """ Test the create_educator function. """
        data = {
            'name': 'Smokey the Bear',
            'work_email': 'smokey@abc.gov',
            'organization_name': 'Wildfire Foundation',
            'org_or_school': 'O',
            'address_line_1': '123 Main St.',
            'address_line_2': None,
            'city': 'Anytown',
            'state': 'CT',
            'zipcode': '20852',
            'num_students': 10,
        }

        educator = create_educator(data)
        self.assertIsNotNone(educator)

        saved = Educator.objects.get(work_email='smokey@abc.gov')
        self.assertEqual(saved.name, data['name'])
        self.assertEqual(saved.organization_name, data['organization_name'])
        self.assertEqual(saved.address_line_1, data['address_line_1'])
        self.assertEqual(saved.address_line_2, data['address_line_2'])
        self.assertEqual(saved.city, data['city'])
        self.assertEqual(saved.state, data['state'])
        self.assertEqual(saved.zipcode, data['zipcode'])
        self.assertEqual(saved.num_students, data['num_students'])
        self.assertEqual(saved.org_or_school, data['org_or_school'])
