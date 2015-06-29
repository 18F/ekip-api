from django.test import TestCase 

from .management.commands.passes import phone_number, name_to_site_type
from .management.commands.slugify import nps_slug, nf_slug, nwr_slug

class DataCleanupTests(TestCase):

    def test_phone_number(self):
        """ Test that the phone, extension parsing works.  """

        phone, extension = phone_number('202-555-7777 ')
        self.assertEqual(phone, '202-555-7777')

        phone, extension = phone_number('340-775-5555 x 238')
        self.assertEqual(phone, '340-775-5555')
        self.assertEqual(extension, '238')

        phone, extension = phone_number('510-792-5555 ext 363')
        self.assertEqual(phone, '510-792-5555')
        self.assertEqual(extension, '363')

        phone, extension = phone_number('973-555-0990 ext. 11')
        self.assertEqual(phone, '973-555-0990')
        self.assertEqual(extension, '11')

        phone, extension = phone_number('580-555-3165; 580-622-3161')
        self.assertEqual(phone, '580-555-3165')

    def test_name_to_site_type(self):
        self.assertEqual(
            'NF',
            name_to_site_type('Angeles NF - LA River District'))
        self.assertEqual(
            'NRA',
            name_to_site_type('Golden Gate NRA - Alcatraz Visitors Center'))
        self.assertEqual(
            'NWR',
            name_to_site_type('Tule Lake NWR'))
        self.assertEqual(
            'NWR',
            name_to_site_type('Kilauea Point National Wildlife Refuge'))
        self.assertEqual(
            'NHS',
            name_to_site_type('Abraham Lincoln Birthplace NHS'))
        self.assertEqual(
            'NPS',
            name_to_site_type('Assateague Island National Seashore'))


class SlugifyTests(TestCase):
    def test_nps_slug(self):
        url = 'http://www.nps.gov/isro/'
        slug = nps_slug(url)
        self.assertEqual(slug, 'nps-isro')

    def test_nf_slug(self):
        name = "Monongahela NF - Main Office"
        slug = nf_slug(name)
        self.assertEqual(slug, 'nf-monongahela-main')

        name = "Monongahela NF - Cranberry Mountain Nature Center"
        slug = nf_slug(name)
        self.assertEqual(slug, 'nf-monongahela-cranberry-mountain-nature')

    def test_nwr_slug(self):
        name = "Texas Midcoast NWR Complex"
        self.assertEqual('nwr-texas-midcoast', nwr_slug(name))

        name = "Tamarac National Wildlife Refuge"
        self.assertEqual('nwr-tamarac', nwr_slug(name))

        name = "Nisqually NWR"
        self.assertEqual('nwr-nisqually', nwr_slug(name))
