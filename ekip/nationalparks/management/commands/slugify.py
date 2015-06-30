from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db.utils import IntegrityError

from nationalparks.models import FederalSite


def delete_from(string, deletes):
    """ Delete the strings in deletes from string. """
    for d in deletes:
        string = string.replace(d, '')
    return string


def nwr_slug(name):
    """ National Wildlife Refuge related slug generation. """
    deletes = [
        'NWRC', 'NWR', 'Complex', 'District', 'National Wildlife Refuge',
        '(also sold at fee booth)', 'National Wildlife & Fish Refuge', 
        'Fish and Wildlife Service']
    name = delete_from(name, deletes)
    return slugify('nwr %s' % name)


def nf_slug(name):
    """ National Forest related slug generation. """

    deletes = [
        'District', 'Office', 'Ranger Station', 'Information Center', 'NF', 
        "Visitor's Center", "Management Unit", 'Visitor Center',
        'Nature Center']
    name = delete_from(name, deletes)
    return slugify('nf %s' % name)


def nps_slug(nps_url):
    """ National Park Service related slug generation. """

    path = urlparse(nps_url).path
    components = [i for i in path.split('/') if i != '']
    return slugify('nps %s' % components[-1])


def blm_slug(name):
    """ BLM related slug generation. """
    deletes = [
        'BLM', 'Field', 'Office', 'District',
        'National', 'Historic', 'Monument']
    name = delete_from(name, deletes)
    return slugify('blm %s' % name)


def nra_slug(name):
    """ National Recreation Area related slug generation. """
    deletes = [
        'NRA', 'Field Office', 'National Recreation Area', 'Fee Machines',
        'Fee Booth', 'Info Site']
    name = delete_from(name, deletes)
    return slugify('nra %s' % name)


def other_slug(name):
    """ Not a specific agency. """
    deletes = [
        'Information Center', 'Visitors Center', 'Area Office',
        'Office', 'Central']
    name = delete_from(name, deletes)
    return slugify('oth %s' % name)


class Command(BaseCommand):
    """ Assign a slug to each FederalSite in the database. """

    def handle(self, *args, **options):
        sites = FederalSite.objects.all()

        slug = ''
        for site in sites:
            if 'nps.gov' in site.website:
                slug = nps_slug(site.website, site.city)
            elif site.site_type == 'NF':
                slug = nf_slug(site.name)
            elif site.site_type == 'NWR':
                slug = nwr_slug(site.name)
            elif site.site_type == 'BLM':
                slug = blm_slug(site.name)
            elif site.site_type == 'NRA':
                slug = nra_slug(site.name)
            else:
                slug = other_slug(site.name)
            site.slug = slug

            try:
                site.save()
            except IntegrityError:
                # It's likely we have a duplicate slug, try adding in the city. 
                slug = slugify("%s %s" % (slug, site.city))
                site.slug = slug
                site.save()
