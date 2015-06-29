from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from nationalparks.models import FederalSite


def delete_from(string, deletes):
    for d in deletes:
        string = string.replace(d, '')
    return string


def nwr_slug(name):
    deletes = ['NWRC', 'NWR', 'Complex', 'National Wildlife Refuge']
    name = delete_from(name, deletes)
    return slugify('nwr %s' % name)


def nf_slug(name):
    name = name.replace('District', '').replace('Office', '')
    name = name.replace('Ranger Station', '')
    name = name.replace('Information', '')
    name = name.replace('Center', '').replace('NF', '').strip()
    return slugify('nf %s' % name)
    

def nps_slug(nps_url):
    """ National Park Service (NPS) urls contain a unique short, slug already.
    Extract that and use it. """

    path = urlparse(nps_url).path
    components = [i for i in path.split('/') if i != '']
    return slugify('nps %s' % components[-1])


def blm_slug(name):
    """ BLM offices """
    deletes = ['BLM', 'Field', 'Office', 'District']
    name = delete_from(name, deletes)
    return slugify('blm %s' % name)

    

class Command(BaseCommand):

    def handle(self, *args, **options):
        sites = FederalSite.objects.all()
        
        slug = ''
        for site in sites:
            if 'nps.gov' in site.website:
                slug = nps_slug(site.website)
            elif site.site_type == 'NF':
                slug = nf_slug(site.name)
            elif site.site_type == 'NWR':
                slug = nwr_slug(site.name)
            else:
                print(site.name)
                print(site.website)
                print(site.site_type)
