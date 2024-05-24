from lxml import etree

def parse() -> etree:
    """Parst das übegebene GPX File und gibt es als Objekt zurück

    Args:
        file: GPX Datei, die geparst werden soll

    Return:
        ET.ElementTree: 
     
    """

    # Später aus Hauptmenu übergeben
    file = "../data/test1.gpx"
    tree = etree.parse(file)
    
    return tree

def write_file(tree: etree) -> etree: 
    tree.write("../data/output.gpx", xml_declaration=True)