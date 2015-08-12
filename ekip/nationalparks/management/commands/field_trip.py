import csv

from django.core.management.base import BaseCommand

def process_site(row):
    print(row['EKIP_VOUCH'])

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
