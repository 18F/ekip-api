import csv

from django.core.management.base import BaseCommand, CommandError
from nationalparks.models import FederalSite

def name_to_site_type(name):
    """ The name of a Federal Site in this list provides an indication of what
    type of site it might be. This extracts that out. """

    if ' BLM' in name:
        site_type = 'BLM'
    elif ' NF' in name:
        site_type = 'NF'
    elif ' NWR' in name:
        site_type = 'NWR'
    elif ' NHS' in name:
        site_type = 'NHS'
    elif ' NRA' in name:
        site_type = 'NRA'
    elif 'National Wildlife Refuge' in name:
        site_type = 'NWR'
    else:
        site_type = 'NPS'
    return site_type

def phone_number(pstr):
    """ Extract the extension from the phone number if it exists. """

    if ' x ' in pstr:
        phone, extension = pstr.split('x')
        return (phone.strip(), extension.strip())
    elif 'ext' in pstr:
        phone, extension = pstr.split('ext')
        return (phone.strip(), extension.strip())
    else:
        return (pstr.strip(), None)

def process_site(row):
    """ Create an entry in the database for a federal site."""

    # Some rows in the CSV don't represent sites. This is indicative by them 
    # missing the city name. 
    if row[2] != '':
        name = row[0]
        phone, phone_extension = phone_number(row[1])
        city = row[2]
        state = row[3]
        website = row[4]
        annual = row[5] == 'YES'
        senior = row[6] == 'YES'
        access = row[7] == 'YES'
        site_type = name_to_site_type(name)

        fs = FederalSite(
            name=name,
            site_type=site_type,
            phone=phone, 
            phone_extension=phone_extension, 
            city=city, 
            state=state,
            website=website, 
            annual_pass=annual, 
            senior_pass=senior,
            access_pass=access)
        fs.save()

     
def read_pass_list(filename):
    with open(filename, 'r', encoding='latin-1') as passcsv:
        passreader = csv.reader(passcsv, delimiter=',')
        for l in passreader:
            process_site(l)


class Command(BaseCommand):
    """ Read and import a pass list. """

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1)

    def handle(self, *args, **options):
        filename = options['filename'][0]
        read_pass_list(filename)
