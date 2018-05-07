#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converts an OSM XML file into JSON files to be imported into MongoDB

Adapted from the data.py module found in the case study quizzes.
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    """
    Convert an XML element into a multi-level dictionary
    :param element: XML element to parse
    :return: Multi-level dictionary suitable for JSON output
    """
    node = {}
    if element.tag == "node" or element.tag == "way":
        # add the tag type to the node dictionary
        node['type'] = element.tag

        # Dump all the attributes from the element into the dictionary
        node.update(element.attrib)

        # Pop CREATED items into the 'created' sub-dictionary
        node['created'] = {k:node.pop(k) for k in CREATED}

        # Capture the latitude and longitude if present
        if 'lat' in node and 'lon' in node:
            node['pos'] = [float(node.pop('lat')), float(node.pop('lon'))]

        # Get the second level tags
        for tag in element.findall('tag'):
            # grab the k and v attributes
            k, v = tag.attrib['k'], tag.attrib['v']

            # skip tag if key contains problem characters
            if problemchars.search(k): continue

            # Break addresses down into a sub-dictionary
            if "addr:" in k:
                if 'address' not in node:
                    node['address'] = {}

                # Parse second portion of name for sub-tdictionary key
                _, k = k.split(':', 1)

                # Replace the remaining colons with underscores
                k = k.replace(':', '_')

                # Special handling for street addresses, using the audit functions
                if k == "street":
                    if audit.over_abbr_re.search(v):
                        v = audit.update_short_name(v)
                    else:
                        v = audit.update_street_name(v)
                node['address'][k] = v
            # deal with remaining tags
            else:
                # Replace any colons with underscores
                k = k.replace(':', '_')

                # Update format of cuisine and phone tag types
                if k == "cuisine":
                    # Python magic: split v to a list and apply update_cuisine to each item
                    v = map(audit.update_cuisine, v.split(';'))
                elif k == "phone":
                    v = audit.update_number(v)
                    if not v:  # When phone number was invalid
                        continue

                # Save the tag
                node[k] = v

        # store nd ref tags for ways
        if element.tag == "way":
            node['node_refs'] = [nd.attrib['ref'] for nd in element.findall('nd')]

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('napoli.osm', False)

    addresses_found = 0
    for tag in data:
        if "phone" in tag:
            pprint.pprint(tag)
            addresses_found += 1
            if addresses_found == 3:
                break

    return


if __name__ == "__main__":
    test()
