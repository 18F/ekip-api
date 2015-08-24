from django.test import TestCase

from ..management.commands import field_trip as trip
from ..models import BestVisitTime, YouthFacility, FieldTripSite


class FieldTripTests(TestCase):
    """ Tests for the importer management command """

    def test_abbreviate_agency(self):
        agency_name = 'Army Corps'
        self.assertEqual('USACE', trip.abbreviate_agency(agency_name))

        agency_name = 'Bureau of Land Management'
        self.assertEqual('BLM', trip.abbreviate_agency(agency_name))

        agency_name = 'Bureau of Reclamation'
        self.assertEqual('USBR', trip.abbreviate_agency(agency_name))

        agency_name = 'National Oceanic and Atmospheric Administration'
        self.assertEqual('NOAA', trip.abbreviate_agency(agency_name))

        agency_name = 'National Park Service'
        self.assertEqual('NPS', trip.abbreviate_agency(agency_name))

        agency_name = 'U.S. Fish and Wildlife Service'
        self.assertEqual('FWS', trip.abbreviate_agency(agency_name))

        agency_name = 'U.S. Forest Service'
        self.assertEqual('FS', trip.abbreviate_agency(agency_name))

    def test_create_best_times(self):
        time_ranges = ['April', 'November - January']
        best_times = trip.create_best_times(time_ranges)

        bvt_april = BestVisitTime.objects.get(best_time='April')
        self.assertIsNotNone(bvt_april)

        bvt_range = BestVisitTime.objects.get(best_time='November - January')
        self.assertIsNotNone(bvt_range)

        april = trip.create_best_times(['April'])
        april = april[0]
        self.assertEqual(bvt_april.id, april.id)

    def test_create_youth_facilities(self):
        youth_facilities = ['Restrooms', 'Visitor Center']
        facilities = trip.create_youth_facilities(youth_facilities)
        self.assertTrue(len(facilities) > 0)

        r1 = YouthFacility.objects.get(facility='Restrooms')
        self.assertIsNotNone(r1)

        r2 = trip.create_youth_facilities(['Restrooms'])
        r2 = r2[0]
        self.assertEqual(r1.id, r2.id)

    def test_process_site(self):
        row = {
            'NAME': ' Wheeler NWR',
            'AGENCY': 'U.S. Fish and Wildlife Service',
            'PHONE_1': '(256) 350-6639',
            'City': 'Decatur',
            'Region': 'Alabama',
            'WEBSITE': 'http;/www.fws.gov/refuge/Wheeler/',
            'StAddr': 'Visitor Center Rd',
            'ADV_RES_RE': 'yes',
            'THRIRTYFIV': 'Yes',
            'PostalCode': '35603',
            'YOUTH_FACI': 'Visitor center, trail, auto tour route, bicycling',
            'BEST_TIMES': 'September through June'}

        trip.process_site(row)

        fts = FieldTripSite.objects.get(slug='fwswheeler-nwr')
        self.assertIsNotNone(fts)

        self.assertEqual('Wheeler National Wildlife Refuge', fts.name)
        self.assertEqual('FWS', fts.agency)
        self.assertEqual('256-350-6639', fts.phone)
        self.assertEqual('http://www.fws.gov/refuge/Wheeler/', fts.website)
        self.assertEqual('Visitor Center Rd', fts.address_line_1)
        self.assertEqual(True, fts.advance_reservation)

        self.assertEqual('Decatur', fts.city)
        self.assertEqual('AL', fts.state)
        self.assertEqual('35603', fts.zipcode)

        best_visit_time = fts.best_visit_times.all()[0]
        self.assertEqual('September - June', best_visit_time.best_time)

        youth_facilities = [y.facility for y in fts.facilities.all()]
        self.assertTrue('visitor center' in youth_facilities)
        self.assertTrue('trail' in youth_facilities)
        self.assertTrue('auto tour route' in youth_facilities)
        self.assertTrue('bicycling' in youth_facilities)
