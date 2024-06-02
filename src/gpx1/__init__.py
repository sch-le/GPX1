""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Leon Schuck
Erstellt: 19.05.2024
"""

from . import parser
from . import waypoints
from lxml import etree

# from . import file_management


def main() -> None:
    input_gpx = parser.parse(r"..//data//test4.gpx")

    waypoints.print_list(input_gpx)
    
    waypoints.calc_elevation(0, 36, input_gpx)
    waypoints.edit(1, 1, 1, 1, input_gpx)
    waypoints.edit(37, 1, None, 1, input_gpx)
   # file_management.openFile()


    #if input_gpx is not None:
     #   parser.write_file(input_gpx)
