from lxml import etree

def parse(file: str) -> etree:
    """Parst das übegebene GPX File und gibt es als Objekt zurück

    Args:
        file: GPX Datei, die geparst werden soll

    Return:
        ET.ElementTree: geparste GPX Daten
    """
    tree = etree.parse(file)

    return tree

def write_file(tree: etree) -> None:
    """Schreibt den übergebenen etree als GPX File

    Args:
        etree: geparste GPX Daten
    """
    # TODO: <?xml ... ?> Informationen anpassen, evtl vorher parsen 
    tree.write("../data/output.gpx", xml_declaration=True)
    