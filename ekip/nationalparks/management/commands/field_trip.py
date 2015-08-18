import csv

from django.core.management.base import BaseCommand

from nationalparks.management.commands import ficorcleaner as fc
from nationalparks.models import FieldTripSite, BestVisitTime, YouthFacility


NAME_TO_ABBR = {r[1]:r[0] for r in FieldTripSite.AGENCY_CHOICES}
NAME_TO_ABBR['Army Corps'] = 'USACE'


def abbreviate_agency(agency_name):
    return NAME_TO_ABBR[agency_name]

def create_youth_facilities(facilities_list):
    facilities = []
    for feature in facilities_list:
        try:
            facility = YouthFacility.objects.get(facility=features)
            facilities.append(facility)
        except: 
            pass


def process_site(row):
    name = fc.clean_name(row['NAME'])
    print('-------------')
    print(name)
    agency = abbreviate_agency(fc.clean_agency(row['AGENCY']))
    phone = fc.clean_phone(row['PHONE_1'])
    city = row['City']
    state = row['Region']
    website = fc.clean_website(row['WEBSITE'])
    address_line_1 = row['AddressLin']
    advance_reservation = fc.clean_advance_reservation(row['ADV_RES_RE'])
    larger_groups = fc.clean_thirty_five_or_more(row['THRIRTYFIV'])

    youth_facilities = fc.clean_youth_facilities(row['YOUTH_FACI'])
    facilities = create_youth_facilities()
    print(youth_facilities)
    print('-----------------')


def read_site_list(filename):
    with open(filename, 'r', encoding='latin-1') as site_csv:
        site_reader = csv.DictReader(site_csv, delimiter=',', quotechar='"')
        for l in site_reader:
            process_site(l)


class Command(BaseCommand):
    """ Read and import a list of field trip sites (also known as the FICOR
    list)."""

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1)

    def handle(self, *args, **options):
        filename = options['filename'][0]
        read_site_list(filename)
