from getset import *
import codecs


def update_name(streetname, streetnamemapping):
    street = street_type_re().search(streetname).group()

    streetname = streetname.replace(street, streetnamemapping[street])

    return streetname


# clean_element function take tag['value'] and tag['key'] as input and return the updated tag values
def clean_element(tag_value, tag_key):
    # clean postcode
    if tag_key == 'postcode':
        if tag_value[0:2] != '85' or len(tag_value) != 5:
            # find postcode start with 'AZ' and remove the 'AZ'
            if tag_value[0:2] == 'AZ':
                tag_value = tag_value[-5:]

                # print (tag_value)

            #  find cases that using full address as postcode and extract the postcode using re module
            else:
                if len(tag_value) > 5:
                    # print(tag.attrib['v'])
                    pc = re.search(r'(85\d{3})', tag_value)
                    if pc:
                        tag_value = pc.group()

    # clean state name, use 'AZ'
    elif tag_key == 'state':
        tag_value = 'AZ'

    # clean street suffix, change abbreviations to full street suffix
    elif tag_key == 'street':
        full_addr = tag_value
        m = street_type_re().search(full_addr)
        if m:
            street_type = m.group()
            if street_type not in get_expected_street_names():
                if street_type in get_street_name_mapping():
                    tag_value = update_name(full_addr, get_street_name_mapping())
    return tag_value


# Clean and shape node or way XML element to Python dict
def shape_element(element, node_attr_fields=get_node_fields(), way_attr_fields=get_way_fields(),
                  problem_chars=get_problem_chars(), default_tag_type='regular'):
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # clean node element
    if element.tag == 'node':
        for primary in element.iter():
            for i in node_attr_fields:
                if i in primary.attrib:
                    node_attribs[i] = primary.attrib[i]
        if len(element) != 0:
            for j in range(0, len(element)):
                childelem = element[j]
                tag = {}
                if not problem_chars.search(childelem.attrib['k']):  # ignore problematic element
                    tag["id"] = element.attrib["id"]
                    tag["type"] = default_tag_type
                    tag['value'] = childelem.attrib['v']
                    if ":" in childelem.attrib['k']:
                        k_and_v = childelem.attrib['k'].split(':', 1)
                        tag["type"] = k_and_v[0]
                        tag["key"] = k_and_v[1]
                        if tag["type"] == 'addr':
                            tag["value"] = clean_element(tag["value"], tag["key"])  # call clean_element function
                    else:
                        tag["key"] = childelem.attrib['k']
                        if tag["type"] == 'addr':
                            tag["value"] = clean_element(tag["value"], tag["key"])
                tags.append(tag)

        return {'node': node_attribs, 'node_tags': tags}

        # handle way element
    elif element.tag == 'way':
        for primary in element.iter():
            for i in way_attr_fields:
                if i in primary.attrib:
                    way_attribs[i] = primary.attrib[i]

        if len(element) != 0:
            for j in range(0, len(element)):
                childelem = element[j]
                tag = {}
                if childelem.tag == 'tag':
                    if not problem_chars.search(childelem.attrib['k']):
                        tag["id"] = element.attrib["id"]
                        tag["type"] = default_tag_type
                        tag["value"] = childelem.attrib['v']
                        if ":" in childelem.attrib['k']:
                            k_and_v = childelem.attrib['k'].split(':', 1)
                            tag["key"] = k_and_v[1]
                            tag["type"] = k_and_v[0]
                            if tag["type"] == 'addr':
                                tag["value"] = clean_element(tag["value"], tag["key"])  # call clean_element function
                        else:
                            tag["key"] = childelem.attrib['k']
                            if tag["type"] == 'addr':
                                tag["value"] = clean_element(tag["value"], tag["key"])  # update tag values
                    tags.append(tag)

                elif childelem.tag == 'nd':
                    # print (childelem.attrib['ref'])
                    way_node = {'id': element.attrib['id'], 'node_id': childelem.attrib['ref'], 'position': j}
                    # print(way_node)
                    way_nodes.append(way_node)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def process_map(file_in):
    with codecs.open(get_nodes_path(), 'wb') as nodes_file, \
            codecs.open(get_node_tags_path(), 'wb') as nodes_tags_file, \
            codecs.open(get_ways_path(), 'wb') as ways_file, \
            codecs.open(get_way_nodes_path(), 'wb') as way_nodes_file, \
            codecs.open(get_way_tags_path(), 'wb') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, get_node_fields())
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, get_node_tags_fields())
        ways_writer = UnicodeDictWriter(ways_file, get_way_fields())
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, get_way_nodes_fields())
        way_tags_writer = UnicodeDictWriter(way_tags_file, get_way_tags_fields())

        nodes_writer.writeheader()

        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
