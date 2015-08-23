import re
from localflavor.us.us_states import US_STATES, US_TERRITORIES

STATES = {name: abbr for abbr, name in US_STATES}
TERRITORIES = {name: abbr for abbr, name in US_TERRITORIES}
STATES.update(TERRITORIES)


def clean_postal_code(postal_code):
    postal_code = postal_code.strip()
    postal_code = int(postal_code)
    if postal_code > 0:
        return postal_code


def clean_text(text):
    text = text.strip()
    if text:
        return text


def clean_advance_reservation(text):
    """ The advance reservation field identifies whether or not advance
    reservations are required to use these facilities (day use areas). If there
    is not recorded answer (blank) we default to 'no reservation required'.
    Returns 'True' if reservation required, False otherwise. """

    text = text.lower()
    if text in ['yes']:
        return True
    if 'registration required' in text:
        return True
    if 'tour request form' in text:
        return True
    if 'call ahead' in text:
        return True
    return False


def clean_agency(agency_name):
    """ Clean up the agency names in the dataset to make them consistent. """

    agency_name = agency_name.strip()
    if 'Oceanic' in agency_name:
        return 'National Oceanic and Atmospheric Administration'
    return agency_name


def replace_facilities(f):
    """ We replace activity, feature descriptions with standardized phrases to
    describe those (for consistency).  """

    exists = [
        'picnic', 'trail', 'day use', 'beach', 'fishing', 'lake', 'hiking']

    for word in exists:
        if word in f:
            return word

    replacements = [
        ('bicyc', 'bicycling'),
        ('bathroom', 'restrooms'),
        ('observation', 'observation area'),
        ('historic', 'historic structures'),
        ('coast', 'coastal areas'),
        ('outdoor classroom', 'outdoor classroom'),
        ('outdoor education', 'outdoor classroom'),
        ('outdoor school', 'outdoor classroom'),
        ('environmental education', 'environmental education facility'),
        (' ee ', ''),
        (' wetl', ''),
        ('advance reservation', ''),
        ('mobile game', ''),
        (' isl', ''),
        ('bilingual', ''),
        ('education guide', ''),
        ('s live', ''),
        ('hmu', ''),
    ]

    for key, rephrased in replacements:
        if key in f:
            return rephrased

    if 'visitor' in f or 'contact station' in f:
        return 'visitor center'
    elif 'auto' in f or 'driving' in f:
        return 'auto tour route'
    elif 'river' in f and 'museum' not in f:
        return 'river'
    elif ' water ' in f or 'waterway' in f:
        return 'water access'
    elif 'camp' in f and 'spy' not in f and 'primitive' not in f:
        return 'camping'
    else:
        return f


def clean_youth_facilities(facilities):
    facilities = facilities.lower()
    facilities = re.split('[;,]|and|&', facilities)
    facilities = [f.strip() for f in facilities]
    facilities = [f.replace('(a.k.a.', '') for f in facilities]
    facilities = [replace_facilities(f) for f in facilities]

    return facilities


def clean_website(url):
    """ In a few instances, the URL was not formatted correctly. We correct
    that here. """

    url = url.replace('http:/www', 'http://www')
    url = url.replace('http;/', 'http://')
    return url


def clean_name(name):
    """" Clean up the name of the location. """
    name = name.strip()
    name = name.replace('NWR', 'National Wildlife Refuge')
    return name


def clean_phone(phone_number):
    """ Phone numbers exist in the dataset in different formats. Standardize to
    a single format. """

    if phone_number:
        phone_pattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})', re.VERBOSE)
        match = phone_pattern.search(phone_number)
        if match:
            components = match.groups()
            return '%s-%s-%s' % components


def clean_thirty_five_or_more(text):
    """ Return True if the location can support more than 35 4th graders.  """

    text = text.lower().strip()
    if text == 'yes' or text == 'y':
        return True
    else:
        return False


def parse_range(times):
    """ Parse a month or season range like: April - November, or Fall through
    Spring. """

    range_pattern = re.compile(r'(\w+)\s+-\s+(\w+)', re.VERBOSE)
    match = range_pattern.findall(times)
    if match:
        return match
    else:
        through_pattern = re.compile(r'(\w+)\s+ through \s+(\w+)', re.VERBOSE)
        match = through_pattern.findall(times)
        return match


def convert_time_ranges(time_ranges, times):
    """ Convert a parsed list of month, season ranges consistent ranges. """

    ranges = ['%s - %s' % r for r in time_ranges]
    return ranges


def clean_best_times(times):
    """ The best times to visit a location are listed in various different ways
    in the dataset. Extract a month or season range and normalize year-round
    mentions, ensuring that the best times have some semblence of consistency.
    """

    times = times.strip()
    if times:
        if ('-' in times
                or 'through' in times) and 'year-round' not in times.lower():
            time_ranges = parse_range(times)
            return convert_time_ranges(time_ranges, times)
        elif 'year' in times.lower() and 'prime' not in times.lower():
            return ['Year-round']
        else:
            return [times]


def clean_state(state_name):
    return STATES[state_name]
