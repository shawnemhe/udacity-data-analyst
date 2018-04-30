#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Creates a dictionary of the tag types and their counts

Taken from Udacity case study quizzes
"""
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict


def count_tags(filename):
    tags = defaultdict(int)
    for _, elem in ET.iterparse(filename):
        tags[elem.tag] += 1
    return tags


def test():
    tags = count_tags('napoli.osm')
    pprint.pprint(dict(tags))


if __name__ == "__main__":
    test()