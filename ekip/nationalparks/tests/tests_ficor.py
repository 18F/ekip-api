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


    def test_clean_best_times(self):
        text = 'year-round'
        self.assertEqual(['Year-round'], fc.clean_best_times(text))

        text = 'Year Around'
        self.assertEqual(['Year-round'], fc.clean_best_times(text))

        text = 'Year-round opportunities'
        self.assertEqual(['Year-round'], fc.clean_best_times(text))

        text = 'Fall (September - October)'
        self.assertEqual(['September - October'], fc.clean_best_times(text))

        text = 'April'
        self.assertEqual(['April'], fc.clean_best_times(text))

        text = 'Peak periods April through November'
        self.assertEqual(['April - November'], fc.clean_best_times(text))

    def test_clean_state(self):
        text = 'New Mexico'
        self.assertEqual('NM', fc.clean_state(text))

        text = 'Florida'
        self.assertEqual('FL', fc.clean_state(text))

        text = 'Puerto Rico'
        self.assertEqual('PR', fc.clean_state(text))
