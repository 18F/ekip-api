from django.test import TestCase

from ..management.commands import ficorcleaner  as fc


class FicorCleanerTests(TestCase):

    def test_clean_advance_reservation(self):

        all_the_ways = [
            'Call ahead for group visits'
            'Registration required for group educational programs'
            'Tour Request Form'
            'yes'
            'Yes']

        for text in all_the_ways:
            self.assertTrue(fc.clean_advance_reservation(text))

        just_say_no = [
            '',
            'no', 
            'No',
            'not required']

        for text in just_say_no:
            self.assertFalse(fc.clean_advance_reservation(text))


    def test_clean_agency(self):

        agency_name = 'National Oceanic and Atmospheric Administration  '

        self.assertEqual(
            'National Oceanic and Atmospheric Administration',
            fc.clean_agency(agency_name))

        agency_name = 'National Oceanic and Atmospheric Administration (NOAA)'
        self.assertEqual(
            'National Oceanic and Atmospheric Administration',
            fc.clean_agency(agency_name))


    def test_clean_website(self):

        url = 'http;//www.usa.gov'
        self.assertEqual('http://www.usa.gov', fc.clean_website(url))

        url = 'http://www.usa.gov'
        self.assertEqual('http://www.usa.gov', fc.clean_website(url))


    def test_clean_phone(self):
        phone_number = 'Chip Baker/276-629-2503'
        self.assertEqual('276-629-2503', fc.clean_phone(phone_number))

        phone_number = '(931) 858-3525'
        self.assertEqual('931-858-3525', fc.clean_phone(phone_number))

        phone_number = '8178861575'
        self.assertEqual('817-886-1575', fc.clean_phone(phone_number))

        phone_number = '817 886 1575'
        self.assertEqual('817-886-1575', fc.clean_phone(phone_number))

    def test_parse_range(self):
        text = 'April - November'
        self.assertEqual([('April', 'November')], fc.parse_range(text))

        text = 'April - November, June - July'
        self.assertEqual(
            [('April', 'November'), ('June', 'July')], fc.parse_range(text))

        text = 'Fall through Spring and other times'
        self.assertEqual([('Fall', 'Spring')], fc.parse_range(text))

        text = 'Fall - Winter'
        self.assertEqual([('Fall', 'Winter')], fc.parse_range(text))
