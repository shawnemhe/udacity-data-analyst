"""Audits an OSM file for errors

Modified from the original audit.py module found in the case study quizzes
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "napoli.osm"

# REGULAR EXPRESSIONS
# Searches for the street type at the beginning of the string, as is the Italian convention
# Also allows for optional Roman numeral prefixes which are sometimes found in Italian street names
#   for example: II Traversa Cappuccini returns only Traversa
street_type_re = re.compile(r'(^(?:IV\s+|V?I{0,3}\s+)?)(\w+)', re.IGNORECASE)
# Finds Roman Numerals (for capitalization checking)
roman_numeral_re = re.compile(r'\bIV\b|\bV?I{1,3}\b', re.IGNORECASE)
# Finds all single letter abbreviations. Returns following word for context.
over_abbr_re = re.compile(r'(\b\w\.\s*)+\w+')

# List of expected street names in the dataset.
expected = ["borgo",
            "calata",
            "circumvallazione",
            "contrada",
            "corso",
            "cupa",
            "discesa",
            "domenico",
            "galleria",
            "gradoni",
            "largo",
            "molo",
            "parco",
            "pendio",
            "piazza", "piazzale", "piazzetta",
            "rampa", "rampe",
            "riviera",
            "salita",
            "san",
            "scale",
            "strada", "stradone",
            "supportico",
            "traversa",
            "via", "viale",
            "vico", "vicolo", "vicoletto"]

# Mapping of street names to be corrected
st_name_mapping = {
    'Prima': 'I',
    'Seconda': 'II',
    'viia': 'Via',
    'Viia': 'Via'
}

# Mapping of abbreviations to full names
abbreviations = {
    "A. De": "Antonio De",
    "A. S. Novaro": "Angelo Silvio Novaro",
    "B. V. Romano": "Beato Vincenzo Romano",
    "G. Di": "Gaspare Di",
    "G. Marotta": "Giuseppe Marotta",
    "G. Melisurgo": "Guglielmo Melisurgo",
    "S. Angelo": "Sant'Angelo",
    "S.Agnese": "Sant'Agnese",
    "S.Ignazio": "Sant'Ignazio"
}

# Mapping of cuisine type corrections
cuisine_types = {
    "italian_pizza": "pizza",
    "regional,_italian": "regional"
}


def audit_street_type(street_types, street_name):
    """
    Populates a dictionary of unexpected street types

    Searches for the street type from a given street name, and then
    verifies that it is an expected street type. If not, adds the street
    type and full street name ot the dictionary.
    :param street_types: dictionary to update
    :param street_name: street name to search
    :return: No return value, dictionary is modified in outer scope
    """
    # search for street name
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group(2)
        if street_type.lower() not in expected:
            # street type unexpected, add to dictionary
            street_types[street_type].add(street_name)


def audit_abbr(over_abbreviated, street_name):
    """
    Populates a dictionary of abbreviations and the streets that contain them
    :param over_abbreviated: dictionary to update
    :param street_name: street name to check for abbreviations
    :return: No return value, dictionary is modified in outer scope
    """
    m = over_abbr_re.search(street_name)
    if m:
        abbr = m.group()
        over_abbreviated[abbr].add(street_name)


def audit_cuisines(cuisines, cuisine_list):
    """
    Splits cuisine values from the dataset and updates a dictionary

    The dataset contains a "cuisine" value that is a semicolon separated list of
    cuisine types. This function splits those values and updates a dictionary that
    tracks a count of how many times each cuisine is found in the dataset
    :param cuisines: dictionary of cuisines to update
    :param cuisine_list: list of cuisines types to process
    :return: No return value, dictionary is modified in outer scope
    """
    for cuisine_type in cuisine_list.split(';'):
        cuisines[cuisine_type] +=1


def audit_phone_numbers(formats, number):
    """
    Audits phone numbers for formatting errors

    The formats dictionary contains mixed types. The end result will
    be a list of numbers containing various character types for informational
    purposes, and 2 lists containing numbers of incorrect lengths or characters.
    These are stored as full lists for closer inspection.
    :param formats: dictionary of invalid formats to populate
    :param number: phone number to validate
    :return: No return value, dictionary is modified in outer scope
    """

    # check formatting
    if re.match(r'^\+39', number):  # starts with +39
        formats['has_country_code'] += 1
    else:
        formats['no_country_code'] += 1
    if re.match(r'^(?:\+?39)?81', number):
        formats['missing_prefix'] += 1
    if re.search('-', number):      # has a dash
        formats['has_dashes'] += 1
    if re.search(r'\s', number):    # contains any whitespace character
        formats['has_spaces'] += 1

    # Strip number to count digits
    digits_only = re.sub(r'[^\d]', '', number)
    # remove country code to count remaining digits
    digits_only = re.sub(r'^39', '', digits_only)
    if not 6 <= len(digits_only) <= 11:
        formats['incorrect_length'].append(number)

    # catch all numbers with unexpected characters
    if re.search(r'[^\+\d\s-]', number):
        formats['bad_chars'].append(number)


def is_street_name(elem):
    """Returns true if tag is a street name"""
    return elem.attrib['k'] == "addr:street"


def is_cuisine(elem):
    """Returns true if tag is a cuisine type"""
    return elem.attrib['k'] == 'cuisine'


def is_phone(elem):
    """Returns true if tag is a phone number"""
    return elem.attrib['k'] == 'phone'


def audit(osmfile):
    """
    Audits
    :param osmfile:
    :return:
    """
    street_types = defaultdict(set)
    over_abbreviated = defaultdict(set)
    cuisines = defaultdict(int)
    phone_numbers = {'has_country_code': 0,
                     'no_country_code': 0,
                     'missing_prefix': 0,
                     'has_dashes': 0,
                     'has_spaces': 0,
                     'incorrect_length': [],
                     'bad_chars': [],
               }

    tags = iterosm(osmfile)
    for tag in tags:
        if is_street_name(tag):
            audit_street_type(street_types, tag.attrib['v'])
            audit_abbr(over_abbreviated, tag.attrib['v'])
        elif is_cuisine(tag):
            audit_cuisines(cuisines, tag.attrib['v'])
        elif is_phone(tag):
            audit_phone_numbers(phone_numbers, tag.attrib['v'])

    tags.close()
    return street_types, over_abbreviated, cuisines, phone_numbers


def iterosm(osmfile, tag_types=('node', 'way')):
    """Creates a generator to yield tag values

    :param osmfile: name of the OpenStreetMap file to iterate
    :param tag_types: type of element tags to iterate
    :return: yields a tag value
    """
    with open(osmfile, 'r') as osm_file:
        for event, elem in ET.iterparse(osmfile, events=('start',)):
            if elem.tag in tag_types:
                for tag in elem.iter('tag'):
                    yield tag


def update_street_name(name):
    # Convert lowercase street names to title case
    if name.islower():
        name = name.title()

    # Find Roman Numerals and make sure they are capitalized
    name = roman_numeral_re.sub(lambda x: str.upper(x.group()), name)

    # retrieve the street type
    m = street_type_re.search(name)
    street_type = m.group(2)
    if street_type in st_name_mapping:
        replacement = r'\1' + st_name_mapping[street_type]
        name = street_type_re.sub(replacement, name)
    elif street_type.islower():
        replacement = r'\1' + street_type.capitalize()
        name = street_type_re.sub(replacement, name)

    return name


def update_short_name(name):
    """Expands an abbreviated name to full length

    :param name: Abbreviated name to expand
    :return: Unabbreviated name
    """
    # First verify that the common errors have been fixed
    name = update_street_name(name)

    # Find the abbreviation to replace
    m = over_abbr_re.search(name)
    if m:
        if m.group() in abbreviations:
            name = over_abbr_re.sub(abbreviations[m.group()], name)

    return name


def update_cuisine(cuisine_type):
    """
    Updates a cuisine type
    :param cuisine_type: type to fix
    :return: corrected cuisine type
    """

    # there is only pizza
    if cuisine_type in cuisine_types.iterkeys():
        return cuisine_types[cuisine_type]
    else:
        return cuisine_type


def update_number(number):
    """
    Corrects number formatting
    :param number: phone number to reformat
    :return: phone number in +<country code><number> format
    """
    # remove non-numeric characters
    number = re.sub(r'[^\d]', '', number)

    # remove country code for length checking
    number = re.sub(r'^39', '', number)

    # Return None if the number is in the incorrect format
    if not 6 <= len(number) <= 11:
        return None

    # Verify landlines include a 0 prefix.
    # A land line is any number not starting with a 3.
    number = re.sub(r'^([^03]\d+)', r'0\1', number)

    # Insert country code
    number = "+39" + number

    return number


def test():
    st_types, over_abbr, cuisines, phone_formats = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    pprint.pprint(dict(over_abbr))
    pprint.pprint(dict(cuisines))
    pprint.pprint(phone_formats)

    for ways in st_types.itervalues():
        for name in ways:
            better_name = update_street_name(name)
            print name, "=>", better_name
    for abbreviated in over_abbr.itervalues():
        for short_name in abbreviated:
            full_name = update_short_name(short_name)
        print short_name, "=>", full_name
    for cuisine_type in cuisines.iterkeys():
        better_cuisine_type = update_cuisine(cuisine_type)
        if cuisine_type != better_cuisine_type:
            print cuisine_type, "=>", better_cuisine_type

    # create a list of sample updated numbers
    sample_numbers = {}
    tags = iterosm(OSMFILE)
    while len(sample_numbers) < 10:
        tag = next(tags)
        if is_phone(tag):
            number = tag.attrib['v']
            sample_numbers[number] = update_number(number)
    else:
        tags.close()
    for old, new in sample_numbers.iteritems():
        print old, "=>", new


if __name__ == '__main__':
    test()
