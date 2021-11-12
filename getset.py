import xml.etree.cElementTree as ET
import re
import csv


def get_osm_filename(osm_file="Phoenix.osm"):
    return osm_file


def get_small_osm(sample_file="PhoenixSmall.osm"):
    return sample_file


def get_med_osm(test_file="PhoenixMed.osm"):
    return test_file


def street_type_re(reg=re.compile(r'\b\S+\.?$', re.IGNORECASE)):
    return reg


def get_expected_street_names(expected=("Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane",
                                        "Road", "Trail", "Parkway", "Commons", "Way", "Circle", "Key", "Terrace",
                                        "Garden")):
    return list(expected)


def get_street_name_mapping(mapping={"St": "Street", "St.": "Street", "Ave": "Avenue", "Ave.": "Avenue", "Rd.": "Road",
                                     "BLVD": "Boulevard", "Dr.": "Drive", "PL": "Place", "Pl": "Place", "Ln": "Lane",
                                     "Ct": "Court", "Blvd": "Boulevard", "Cir": "Circle", "Dr": "Drive"}):
    return mapping


def get_nodes_path(nodes_path="nodes.csv"):
    return nodes_path


def get_node_tags_path(node_tags_path="node_tags.csv"):
    return node_tags_path


def get_ways_path(ways_path="ways.csv"):
    return ways_path


def get_way_nodes_path(way_nodes_path="way_nodes.csv"):
    return way_nodes_path


def get_way_tags_path(way_tags_path="way_tags.csv"):
    return way_tags_path


def get_problem_chars(problem_chars=re.compile(r'[=+/&<>;\'"?%#$@,. \t\r\n]')):
    return problem_chars


def get_node_fields():
    output = ('id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp',)
    return output


def get_node_tags_fields():
    output = ('id', 'key', 'value', 'type',)
    return output


def get_way_fields():
    output = ('id', 'user', 'uid', 'version', 'changeset', 'timestamp',)
    return output


def get_way_tags_fields():
    output = ('id', 'key', 'value', 'type',)
    return output


def get_way_nodes_fields():
    output = ('id', 'node_id', 'position')
    return output


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow(
            {k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()})

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, conroot = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            conroot.clear()


# create samples of original osm
def sample_data(large=get_osm_filename(), small=get_small_osm(), medium=get_med_osm()):
    k = 10000  # Parameter: take every k-th top level element, take small sample
    m = 100  # take intermediate sample
    with open(small, 'wb') as output1, open(medium, 'wb') as output2:
        output1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output1.write('<osm>\n  ')
        output2.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output2.write('<osm>\n  ')
        # Write every kth and mth top level element
        for i, element in enumerate(get_element(large)):
            if i % k == 0:
                output1.write(str(ET.tostring(element, encoding='utf-8')))
                output2.write(str(ET.tostring(element, encoding='utf-8')))
            elif i % m == 0:
                output2.write(str(ET.tostring(element, encoding='utf-8')))
        output1.write('</osm>')
        output2.write('</osm>')
