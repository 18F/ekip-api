from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .views import issue_single_voucher, STATES
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
