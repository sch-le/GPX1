""" parser.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum parsen und ausgeben von GPX-Dateien
Autor: Leon Schuck
Erstellt: 19.05.2024
"""

from lxml import etree
import re
import sys

from gpx1.config import gpx
from gpx1.usefull import print_error

def parse(file_input: str) -> gpx:
    """Parst das übegebene GPX File und gibt es als Objekt zurück

    Args:
        file_input (str): GPX Datei, die geparst werden soll

    Returns:
        gpx: geparste GPX-Daten und XML-Deklarationen
    """ 

    gpx_input = gpx()

    try:
        # Auslesen der XML-Deklarationen
        with open(file_input, "r") as f:
            gpx_input.encoding = f.encoding

            # Suchen nach der standalone Deklarierung in der ersten Zeilen der Datei
            gpx.standalone = re.search ("standalone=\"(.+)\"",f.readline())

        # Auslesen der GPX-Daten
        gpx_input.etree = etree.parse(file_input)
        
        return gpx_input
    except Exception as e:
        print_error("Error 100: Fehler beim parsen der GPX-Datei: " + e, True, True)
        sys.exit()

def write_file(gpx_output: gpx, path: str) -> None:
    """Erstellt aus den übergebenen GPX-Informationen eine .gpx Datei

    Args:
        gpx_output (gpx): zu speichernde GPX-Daten und XML-Deklarationen
        path (str): Pfad und Name unter der die Datei ausgegeben werden soll
    """    
    
    # Ausgabe des GPX-Files
    if gpx_output.standalone is None:
        gpx_output.etree.write(path, xml_declaration=True, encoding=gpx_output.encoding)
    else:
        gpx_output.etree.write(path, xml_declaration=True, encoding=gpx_output.encoding, standalone=gpx_output.standalone)