"""
...
"""

from . import parser

gpx_tree = parser.parse("../data/test1.gpx")
parser.write_file(gpx_tree)
