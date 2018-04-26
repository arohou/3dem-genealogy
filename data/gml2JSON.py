# -*- coding: utf-8 -*-
"""
gml2JSON.py

Standalone Script
Convert 3D Cryo EM Genealogy .gml file from yEd to JSON
JSON content meant for http://bl.ocks.org/eyaler/10586116

John Henry J. Scott
2018-04-26

"""

from networkx import read_gml, node_link_data
from networkx import convert_node_labels_to_integers
from json import dump

gmlFileName = "3dem_genealogy_2018-01-11.gml"
JSONFileName = "3dem_genealogy_2018-01-11.json"

rawgml = read_gml(gmlFileName)

# bl.ocks.org/eyaler/10586116 needs integer id in link syntax
gml = convert_node_labels_to_integers(rawgml)

nd = node_link_data(gml)

# nd['nodes'] is a list of nodes, each node being a dict
# nd['nodes'][3] is a dict
# nd['nodes'][3]['LabelGraphics']['fontSize'] is an int indicating importance

# iterate over all nodes; pull out needed info; and fix up the dict structure
for node in nd['nodes']:
    size = node['LabelGraphics']['fontSize']
    name = node['LabelGraphics']['text']
    type = 'square'
    if (size > 14):
        type = 'circle'
    score = 1

# create keys needed by bl.ocks.org/eyaler/10586116
    node['size'] = size
    node['type'] = type
    node['score'] = score
    node['id'] = name

# delete keys not understood by bl.ocks.org/eyaler/10586116  
    if 'LabelGraphics' in node:
        del node['LabelGraphics']
    if 'graphics' in node:
        del node['graphics']
        
# iterate over all links to delete unwanted key
for link in nd['links']:
    if 'graphics' in link:
        del link['graphics']
    if 'edgeAnchor' in link:
        del link['edgeAnchor']

# fix top-level JSON object
nd['graph'] = []
nd['directed'] = False

# write fixed-up graph to JSON file
fp = open(file=JSONFileName, mode='w')
dump(nd, fp, indent="\t")
fp.close()

