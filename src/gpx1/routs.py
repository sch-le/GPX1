"""routs.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Routs
Autor: Lukas Reißmann
Erstellt: 07.06.2024
"""

from gpx1.config import gpx
from gpx1.usefull import print_color
import lxml

def _get_rtes(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Routen

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Routen
    """
    
    rtes = []
    i = 0

    # Loop über alle "rte" Elemente
    for rte in input_gpx.etree.findall("{*}rte"):
        rtes.append([])
        name = rte.find("{*}name").text
        rtes[i].append(name)
        rtes[i].append([])

    return rtes

def print_rtes(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routen aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Name")
    print_color("--------|--------")
    
    rtes = _get_rtes(input_gpx)
    
    
    for id, rte in enumerate(rtes):
        print_color(f"  {id:4}  |  {rte[0]}")

def _get_rtepts(id: int, input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Routenpunkten und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        id (int): Index der Route in der Liste
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    rtes = _get_rtes(input_gpx)
    
    # Überprüfen, ob die übergebene ID gültig ist
    if id < 0 or id >= len(rtes):
        raise ValueError("Ungültige ID für Route")
    
    rtepts = []
    
    # Finden der spezifischen Route mit der angegebenen ID
    rte_element = input_gpx.etree.findall("{*}rte")[id]
    
    # Durchsuchen aller rtept-Elemente unterhalb des richtigen rte-Elements
    for rtept in rte_element.findall("{*}rtept"):
        # Auslesen der Latitude und Longitude aus den Attributen "lat" und "lon"
        lat = float(rtept.get("lat"))
        lon = float(rtept.get("lon"))
        
        # Hinzufügen der optionalen Elevation als Child-Element "ele", falls vorhanden
        ele = rtept.findtext("{*}ele", default="")
        ele = float(ele) if ele else None
        
        rtepts.append([lat, lon, ele])
    
    return rtepts

def print_list_rtepts(id: int, input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routenpunkten und der dazugehörigen Latitude Longitude und optinalen Elevation aus

    Args:
        id (int): Index der Route in der Liste
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation")
    print_color("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Routenpunkten
    rtepts = _get_rtepts(id, input_gpx)
    
    # Überprüfen, ob Routenpunkte vorhanden sind
    if not rtepts:
        print_color("Keine Routenpunkte für die angegebene Route gefunden.")
        return
    
    # Ausgabe der Routenpunkt Informationen in Listenform
    for id, rpt in enumerate(rtepts):
        print_color(f"  {id:04}  |  {rpt[0]:9.6f} |  {rpt[1]:9.6f}  | {rpt[2]:9.6f}")

def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Routenpunkte zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    rtes = _get_rtes(input_gpx)
    
    return len(rtes)

def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
    """Ändert die Latitude, Longitude und Elevation eines gegebenen Routenpunktes
 
    Args:
        id (int): ID der zu bearbeitenden Routenpunkte
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        gpx: Bearbeitete GPX-Daten
    """
    
    rtepts = _get_rtepts(id, input_gpx)

    if not (0 <= id < len(rtepts)):
        print_color("Error 204: Routenpunkt nicht vorhanden!")
        return input_gpx
    
    # Suchen des bestimmten Elements "rtept"
    rpt = rtepts.findall("{*}rtept")[id]
    
    # Ändern der Latitude und Longitude, über die Attribute "lat" und "lon"
    if lat is not None:
        rpt.set("lat", str(lat))
        
    if lon is not None:
        rpt.set("lon", str(lon))
    
    if ele is not None:
        ele_element = rpt.find("{*}ele")
        if ele_element is not None:
            ele_element.text = str(ele)
        else:
            # Erstellen des Child-Elements "ele"
            ele_element = etree.Element("ele")
            ele_element.text = str(ele)
            rpt.append(ele_element)
    
    return input_gpx

def print_startpoint(id: int, input_gpx: gpx) -> None:
    """Gibt den Startpunkt einer geschlossenen Route aus.

    Args:
        id (int): Index der Route in der Liste
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    rtepts = _get_rtepts(input_gpx)
    
    if not (0 <= id < len(rtepts)):
        print_color("Error 204: Routenpunkt nicht vorhanden!")
        return
    
    
    startpoint = rtepts[id]

    
    print_color("Momentaner Startpunkt")
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation")
    print_color("--------|------------|-------------|-------------")
    print_color(f"  {id:04}  |  {startpoint.get('lat', 'N/A'):9.6f} |  {startpoint.get('lon', 'N/A'):9.6f}  | {startpoint.findtext('{*}ele', 'N/A'):9.6f}")

    

def edit_startpoint(lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
    """Ändert den Startpunkt einer geschlossenen Route.

    Args:
        lat (float): Neue Breitengrad-Koordinate für den Startpunkt
        lon (float): Neue Längengrad-Koordinate für den Startpunkt
        ele (float): Neue Höhenangabe für den Startpunkt
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        gpx: Bearbeitete GPX-Daten
    """
    
    rtepts = _get_rtepts(input_gpx)

    if not rtepts:
        print_color("Error: No route points found!")
        return input_gpx
    
    # Auswählen des ersten Routenpunktes
    startpoint = rtepts[0]
   
    # Editen von lat und lon
    if lat is not None:
        print(f"Neue Breitengrad-Koordinate für den Startpunkt: {lat}")
        startpoint.set("lat", str(lat))
        
    if lon is not None:
        print(f"Neue Längengrad-Koordinate für den Startpunkt: {lon}")
        startpoint.set("lon", str(lon))
    
    if ele is not None:
        print(f"Neue Höhenangabe für den Startpunkt: {ele}")
        ele_element = startpoint.find("{*}ele")
        if ele_element is not None:
            ele_element.text = str(ele)
        else:
            # Erstellen des Child-Elements "ele"
            ele_element = etree.Element("ele")
            ele_element.text = str(ele)
            startpoint.append(ele_element)
    
    return input_gpx

