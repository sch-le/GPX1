""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Leon Schuck
Erstellt: 19.05.2024
"""

from . import parser

input_gpx = parser.parse("../data/test1.gpx")

if input_gpx is not None:
    parser.write_file(input_gpx)
