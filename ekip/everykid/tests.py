from django.test import TestCase, Client

class BasicPageTestCase(TestCase):
    
    def test_main_page(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(200, response.status_code)
