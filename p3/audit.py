"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample.osm"
# Searches for the street type at the beginning of the string, as is the Italian convention
# Also finds and ignores Roman numeral prefixes which are sometimes found in Italian street names
#   for example: II Traversa Cappuccini returns only Traversa
street_type_re = re.compile(r'(^(?:IV\s+|V?I{0,3}\s+)?)(\w+)', re.IGNORECASE)
# finds Roman Numerals (for capitalization checking)
roman_numeral_re = re.compile(r'\bIV\b|\bV?I{1,3}\b', re.IGNORECASE)
# finds all single letter abbreviations
over_abbr_re = re.compile(r'\b\w\.')


expected = ["calata",
            "corso",
            "largo",
            "parco",
            "piazza", "piazzale", "piazzetta",
            "salita",
            "strada",
            "traversa",
            "via", "viale",
            "vico", "vicolo", "vicoletto"]

# The most common issue with street names was capitalization
mapping = {
    'viia': 'Via',
    'Viia': 'Via'
}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group(2)
        if street_type.lower() not in expected:
            street_types[street_type].add(street_name)


def audit_abbr(over_abbreviated, street_name):
    m = over_abbr_re.search(street_name)
    if m:
        abbr = m.group()
        over_abbreviated[abbr].add(street_name)


def audit_cuisines(cuisines, cuisine_list):
    for cuisine_type in cuisine_list.split(';'):
        cuisines[cuisine_type] +=1


def audit_phone_numbers(formats, number):
    """Audits phone numbers for formatting errors

    :param formats: dictionary of invalid formats to populate
    :param number: phone number to validate
    """
    wrong_format = []

    # check formatting
    if re.match(r'^\+39', number):  # starts with +39
        formats['has_country_code'] += 1
    else:
        formats['no_country_code'] += 1
    if re.search('-', number):      # has a dash
        formats['has_dashes'] += 1
    if re.search(r'\s', number):    # contains any whitespace character
        formats['has_spaces'] += 1

    # Strip number to count digits
    digits_only = re.sub(r'[^\d]', '', number)
    if not 6 <= len(digits_only) <= 13:
        formats['incorrect_length'] += 1
        wrong_format.append(digits_only)

    # catch all numbers with unexpected characters
    if re.search(r'[^\+\d\s-]', number):
        wrong_format.append(number)


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
               'has_dashes': 0,
               'has_spaces': 0,
               'incorrect_length': 0 # should be 12 including country code
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


def update_street_name(name, mapping):
    # Convert lowercase street names to title case
    if name.islower():
        name = name.title()

    # Find Roman Numerals and make sure they are capitalized
    name = roman_numeral_re.sub(lambda x: str.upper(x.group()), name)

    # retrieve the street type
    m = street_type_re.search(name)
    street_type = m.group(2)
    if street_type in mapping:
        replacement = r'\1' + mapping[street_type]
        name = street_type_re.sub(replacement, name)
    elif street_type.islower():
        replacement = r'\1' + street_type.capitalize()
        name = street_type_re.sub(replacement, name)

    return name


def update_cuisine(cuisine_type):
    """
    Updates a cuisine type
    :param cuisine_type: type to fix
    :return: corrected cuisine type
    """

    # there is only pizza
    if re.search('pizza', cuisine_type, re.IGNORECASE):
        cuisine_type = 'pizza'

    return cuisine_type


def test():
    st_types, over_abbr, cuisines, phone_formats = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    pprint.pprint(dict(over_abbr))
    pprint.pprint(dict(cuisines))
    pprint.pprint(phone_formats)

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_street_name(name, mapping)
            print name, "=>", better_name
    for cuisine_type in cuisines.iterkeys():
        better_cuisine_type = update_cuisine(cuisine_type)
        if cuisine_type != better_cuisine_type:
            print cuisine_type, "=>", better_cuisine_type


if __name__ == '__main__':
    test()
