import csv

from django.core.management.base import BaseCommand

from nationalparks.management.commands import ficorcleaner as fc
from nationalparks.models import FieldTripSite, BestVisitTime, YouthFacility

#Begin by cleaning house!
try:
    FieldTripSite.objects.all().delete()
    BestVisitTime.objects.all().delete()
    YouthFacility.objects.all().delete()
except:
    pass
    
NAME_TO_ABBR = {r[1]: r[0] for r in FieldTripSite.AGENCY_CHOICES}
NAME_TO_ABBR['Army Corps'] = 'USACE'


def abbreviate_agency(agency_name):
    """ Abbreviate the name of the agency for storage. """
    return NAME_TO_ABBR[agency_name]


def create_best_times(best_times_list):
    """ Create the best visit times objects. """
    best_times = []
    for time_range in best_times_list:
        best_time, _ = BestVisitTime.objects.get_or_create(
            best_time=time_range)
        best_times.append(best_time)
    return best_times


def create_youth_facilities(facilities_list):
    """ Create the youth facilities objects. """
    facilities = []
    for feature in facilities_list:
        facility, _ = YouthFacility.objects.get_or_create(facility=feature)
        facilities.append(facility)
    return facilities


def process_site(row):
    """ Clean up the data, and save a FieldTrip object. """
    name = fc.clean_name(row['NAME'])
    agency = abbreviate_agency(fc.clean_agency(row['AGENCY']))

    field_trip_site, created = FieldTripSite.objects.get_or_create(
        name=name, agency=agency)

    field_trip_site.phone = fc.clean_phone(row['PHONE'])
    field_trip_site.city = fc.clean_text(row['CITY'])
    field_trip_site.state = fc.clean_state(row['STATE'])
    field_trip_site.address_line_1 = fc.clean_text(row['ADDRESS'])
    field_trip_site.zipcode = fc.clean_postal_code(row['ZIPCODE'])
    field_trip_site.website = fc.clean_website(row['WEBSITE'])
    field_trip_site.advance_reservation = fc.clean_advance_reservation(
        row['ADVANCE_RESERVATION'])
        
    field_trip_site.larger_groups = fc.clean_thirty_five_or_more(
        row['THIRTY_FIVE'])
    field_trip_site.save()

    # Clear old data for this facility
    field_trip_site.facilities.remove()

    youth_facilities = fc.clean_youth_facilities(row['YOUTH_FACILITIES'])
    yfacilities = create_youth_facilities(youth_facilities)
    field_trip_site.facilities.add(*yfacilities)

	# Clear old data for this facility
    field_trip_site.best_visit_times.remove()
    
    best_times_data = fc.clean_best_times(row['BEST_TIMES'])
    if best_times_data:
        best_times = create_best_times(best_times_data)
        field_trip_site.best_visit_times.add(*best_times)

    field_trip_site.save()


def read_site_list(filename):
    """ Read and process the list of field trip sites. """
    with open(filename, 'r', encoding='utf-8', errors='strict') as site_csv:
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
