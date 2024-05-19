import xml.etree.ElementTree as ET

def parse() -> ET.ElementTree:
    """Parst das übegebene GPX File und gibt es als Objekt zurück

    Args:
        file: GPX Datei, die geparst werden soll

    Return: 
        ET.ElementTree: 
     
    """

    # Später aus Hauptmenu übergeben
    file = "../data/test1.gpx"
    
    # Namespaces
    ET.register_namespace("", "http://www.topografix.com/GPX/1/1")
    ET.register_namespace("gpxx" ,"http://www.garmin.com/xmlschemas/GpxExtensions/v3")

    # Parsen des GPX Files
    tree = ET.parse(file)
    print(tree)

    tree.write("../data/output.gpx", xml_declaration=True)