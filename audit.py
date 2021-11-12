# import xml.etree.cElementTree as ET
from getset import *


def audit_address(filename):
    postcode_key = 'addr:postcode'
    street_key = 'addr:postcode'
    state_key = 'addr:state'
    city_key = 'addr:city'
    county_key = 'addr:county'

    postcode_types = {}
    street_types = {}
    state_types = {}
    city_types = {}
    county_types = {}

    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == postcode_key:
                    if not re.search(r"^8[56]\d{3}-?(\d{4})?$", tag.attrib['v']):
                        if tag.attrib['v'] in postcode_types:
                            postcode_types[tag.attrib['v']] += 1
                        else:
                            postcode_types[tag.attrib['v']] = 1
                elif tag.attrib['k'] == street_key:
                    m = street_type_re().search(tag.attrib['v'])
                    if m:
                        street_type = m.group()
                        if street_type not in get_expected_street_names():
                            street_types[street_type] = street_types.get(street_type, 0) + 1
                elif tag.attrib['k'] == state_key:
                    state_types[tag.attrib['v']] = state_types.get(tag.attrib['v'], 0) + 1
                elif tag.attrib['k'] == city_key:
                    city_types[tag.attrib['v']] = city_types.get(tag.attrib['v'], 0) + 1
                elif tag.attrib['k'] == county_key:
                    county_types[tag.attrib['v']] = county_types.get(tag.attrib['v'], 0) + 1

    print '\nPostcodes out of norm:\n', postcode_types, \
        '\nStreets out of norm:\n', street_types, \
        '\nStates:\n', state_types, \
        '\nCities:\n', city_types, \
        '\nCounties:\n', county_types
