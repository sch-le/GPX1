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
        print_color(f"  {id:4}  |  {rte[id]}")


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
    
    rte = rtes[id]
    
    rtepts = []
    
    # Durchsuchen aller rtept-Elemente in der gesamten GPX-Datei
    for rtept in input_gpx.etree.findall(".//{*}rtept"):
        # Überprüfen, ob das rtept-Element unterhalb des richtigen rte-Elements liegt
        if rtept.getparent() == rte:
            # Auslesen der Latitude und Longitude aus den Attributen "lat" und "lon"
            lat = float(rtept.get("lat"))
            lon = float(rtept.get("lon"))
            
            # Hinzufügen der optionalen Elevation als Child-Element "ele", falls vorhanden
            ele = rtept.findtext("{*}ele", default="")
            ele = float(ele) if ele else None
            
            rtepts.append([lat, lon, ele])
    
    return rtepts
def print_list_rtepts(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routenpunkte und der dazugehörigen Latitude Longitude und optinalen Elevation aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation")
    print_color("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Routenpunkt
    rtepts = _get_rtepts(input_gpx)
    
    # Ausgabe der Routenpunkt Informationen in Listenform
    for id, rpt in enumerate(rtepts):
        if rpt[2] != "":
            print_color(f"  {id:04}  |  {rpt[0]:9.6f} |  {rpt[1]:9.6f}  | {rpt[2]:9.6f}")
        else:
            print_color(f"  {id:04}  |  {rpt[0]:9.6f} |  {rpt[1]:9.6f}  | {rpt[2]} ")

def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Routenpunkte zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    rtes = _get_rtes(input_gpx)
    
    return len(rtes)

def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
    """Ändert die Latitude, Longitude und Elevation eines gegebenen Routenpunkte
 
    Args:
        id (int): ID des zu bearbeitenden Routenpunkte
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        gpx: Bearbeitete GPX-Daten
    """
    
    rtepts = _get_rtepts(input_gpx)

    if not (0 <= id < len(rtepts)):
        print_color("Error 204: Routenpunkt nicht vorhanden!")
        return input_gpx
    
    # Suchen des bestimmten Elements "rtept"
    rpt = input_gpx.etree.findall("{*}rte/{*}rtept")[id]
    
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
    
    print_rtepts(input_gpx)
    return input_gpx

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
        print_color("Error: Keine Routenpunkte vorhanden!")
        return input_gpx

    # Das erste "rtept"-Element auswählen, um den Startpunkt zu ändern
    startpoint = input_gpx.etree.find("{*}rte/{*}rtept")
    
    # Überprüfen, ob ein Startpunkt vorhanden ist
    if startpoint is None:
        print_color("Error: Kein Startpunkt vorhanden!")
        return input_gpx
    
    # Ändern der Breiten- und Längengrade des Startpunkts
    startpoint.set("lat", str(lat))
    startpoint.set("lon", str(lon))
    
    # Ändern der Elevation, falls vorhanden, oder erstellen, falls nicht vorhanden
    ele_element = startpoint.find("{*}ele")
    if ele_element is not None:
        ele_element.text = str(ele)
    else:
        ele_element = etree.Element("ele")
        ele_element.text = str(ele)
        startpoint.append(ele_element)
    
    # Rückgabe der bearbeiteten GPX-Daten
    return input_gpx

