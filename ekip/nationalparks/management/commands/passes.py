import csv

from django.core.management.base import BaseCommand
from nationalparks.models import FederalSite


def determine_site_type(name, website):
    """ The name (or website)  of a Federal Site in this list provides an
    indication of what type of site it might be. This extracts that out. """

    name_fragments = [
        (' BLM', 'BLM'), (' NF', 'NF'), ('National Forest', 'NF'),
        (' NWR', 'NWR'), (' NHS', 'NHS'), (' NRA', 'NRA'),
        ('National Recreation Area', 'NRA'), 
        ('National Wildlife Refuge', 'NWR'), ('Fish and Wildlife', 'NWR')]

    for fragment, code in name_fragments:
        if fragment in name:
            return code

    website_fragments = [
        ('fs.fed.us', 'NF'), ('fs.usda.gov', 'NF'),
        ('blm.gov', 'BLM'), ('fws.gov', 'NWR'), ('nps.gov', 'NPS')]

    for fragment, code in website_fragments:
        if fragment in website:
            return code

    return 'OTH'


def phone_number(pstr):
    """ Extract the extension from the phone number if it exists. """

    if ';' in pstr:
        # In one case we have multiple phone numbers separated by a
        # semi-colon. We simply pick the first one. Note this means we're
        # "throwing away" the other phone numbers.
        pstr = pstr.split(';')[0]

    for m in [' x ', 'ext.', 'ext']:
        if m in pstr:
            phone, extension = pstr.split(m)
            return (phone.strip(), extension.strip())
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
        site_type = determine_site_type(name, website)

        sites = FederalSite.objects.filter(name=name, city=city)

        if len(sites) > 0:
            # If we encounter a duplicate, let's update instead of inserting.
            fs = sites[0]
        else:
            fs = FederalSite()

        fs.name = name
        fs.site_type = site_type
        fs.phone = phone
        fs.phone_extension = phone_extension
        fs.city = city
        fs.state = state
        fs.website = website
        fs.annual_pass = annual
        fs.senior_pass = senior
        fs.access_pass = access
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
