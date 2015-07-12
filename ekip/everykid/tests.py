from django.test import TestCase, Client
from django.core.urlresolvers import reverse


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


class PassExchangeSiteTestCase(TestCase):
    fixtures = ['federalsites.json']

    def test_choose_by_state(self):
        c = Client()
        response = c.get('/plan-your-trip/pass-exchange/?state=AZ')
        content = response.content.decode('utf-8')
        self.assertTrue('Aqua Fria National Monument' in content)
