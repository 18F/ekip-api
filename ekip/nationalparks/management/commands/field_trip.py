import csv

from django.core.management.base import BaseCommand

from nationalparks.management.commands import ficorcleaner as fc
from nationalparks.models import FieldTripSite, BestVisitTime, YouthFacility


NAME_TO_ABBR = {r[1]: r[0] for r in FieldTripSite.AGENCY_CHOICES}
NAME_TO_ABBR['Army Corps'] = 'USACE'


def abbreviate_agency(agency_name):
    return NAME_TO_ABBR[agency_name]


def create_best_times(best_times_list):
    best_times = []
    for time_range in best_times_list:
        best_time, _ = BestVisitTime.objects.get_or_create(
            best_time=time_range)
        best_times.append(best_time)
    return best_times


def create_youth_facilities(facilities_list):
    facilities = []
    for feature in facilities_list:
        facility, _ = YouthFacility.objects.get_or_create(facility=feature)
        facilities.append(facility)
    return facilities


def process_site(row):
    print(row['BEST_TIMES'])

def process_site2(row):
    name = fc.clean_name(row['NAME'])
    agency = abbreviate_agency(fc.clean_agency(row['AGENCY']))

    field_trip_site, created = FieldTripSite.objects.get_or_create(
        name=name, agency=agency)

    field_trip_site.phone = fc.clean_phone(row['PHONE_1'])
    field_trip_site.city = fc.clean_text(row['City'])
    field_trip_site.state = fc.clean_state(row['Region'])
    field_trip_site.website = fc.clean_website(row['WEBSITE'])
    field_trip_site.address_line_1 = fc.clean_text(row['StAddr'])
    field_trip_site.advance_reservation = fc.clean_advance_reservation(
        row['ADV_RES_RE'])

    field_trip_site.larger_groups = fc.clean_thirty_five_or_more(
        row['THRIRTYFIV'])
    field_trip_site.zipcode = fc.clean_postal_code(row['PostalCode'])
    field_trip_site.save()

    # Clear the deck.
    field_trip_site.best_visit_times.remove()
    field_trip_site.facilities.remove()

    youth_facilities = fc.clean_youth_facilities(row['YOUTH_FACI'])
    yfacilities = create_youth_facilities(youth_facilities)
    field_trip_site.facilities.add(*yfacilities)

    best_times_data = fc.clean_best_times(row['BEST_TIMES'])
    if best_times_data:
        best_times = create_best_times(best_times_data)
        field_trip_site.best_visit_times.add(*best_times)

    field_trip_site.save()


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
