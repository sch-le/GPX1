"""routs.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Routs
Autor: Lukas Reißmann
Erstellt: 07.06.2024
"""

from gpx1.config import gpx
from gpx1.usefull import print_color, print_error
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

    # Suchen aller Routen(rte) in dem GPX-File
    for rte in input_gpx.etree.findall("{*}rte"):
        # Hinzufügen einer weiteren Liste zu jedem Listelement in rtes
        rtes.append([])
        # Suchen nach Namen der Route und hinzufügen einer weiteren Liste für GPS-Daten einzelner Routenpunkte 
        name = rte.find("{*}name").text
        rtes[i].append(name)
        rtes[i].append([])
        # Suchen einzelner Routenpunkte
        for rtept in rte.findall("{*}rtept"):
            lat = float(rtept.get("lat"))
            lon = float(rtept.get("lon"))
            ele = ""
            if rtept.find("{*}ele") is not None:
                ele = float(rtept.find("{*}ele").text)
            
            # Hinzufügen der GPS-Daten der Routenpunkte zu zuvor erstellter Liste
            rtes[i][1].append([lat, lon, ele])
            
        i = i + 1
        

    return rtes

def print_rtes(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routen aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Name")
    print_color("--------|--------")
    
    # Erstellen einer Liste der Routen
    rtes = _get_rtes(input_gpx)

    '''# Überprüfen ob Routen vorhanden sind
    if not rtes:
        print_color("Keine Routen in angegebener Datei gefunden.")
        return
    '''
    
    for id, rte in enumerate(rtes):
        print_color(f"  {id:4}  |  {rte[0]}")


def print_list_rtepts(rte: int, input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routenpunkten und der dazugehörigen Latitude Longitude und optinalen Elevation aus

    Args:
        id (int): Index der Route in der Liste
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation")
    print_color("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Routenpunkten
    rtes = _get_rtes(input_gpx)
    
    
    # Ausgabe der Routenpunkt Informationen in Listenform
    for id, rtept in enumerate(rtes[rte][1]):
        if rtept[2] != "":
            print_color(f"  {id: 4}  | {rtept[0]: 10.6f} | {rtept[1]: 11.6f} |  {rtept[2]: 9.3f}  " ) 
        else:                            
            print_color(f"  {id: 4}  | {rtept[0]: 10.6f} | {rtept[1]: 11.6f} |             ")
              
    return True

def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Routenpunkte zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    rtes = _get_rtes(input_gpx)
    
    return len(rtes)

def edit(rte_id: int, rtept_id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
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
    
    rtes = _get_rtes(input_gpx)

    # Überprüfung ob Routenpunkt existiert
    if rtept_id is None:
        print_error("Error 405: Kein Routenpunkt ausgewählt!")
        return
    
    if not (0 <= rtept_id < len(rtes[rte_id][1])):
        print_error("Error 404: Routenpunkt nicht vorhanden!")
        return
    
    # Suchen nach bestimmten Routenpunkt
    rte = input_gpx.etree.findall("{*}rte")[rte_id]
    rtept = rte.findall("{*}rtept")[rtept_id]
    
    # Ändern der Latitude und Longitude, über die Attribute "lat" und "lon"
    if lat is not None:
        # Bereichsüberprüfung der Latitude
        if not (-90 <= lat <= 90):
            print_error("Error 402: Latitude außerhalb des erlaubten Bereichs!  0 <= Latitude <= 90")
            return
        rtept.set("lat", str(lat))
        
    if lon is not None:
        # Bereichsüberprüfung der Longitude
        if not (-180 <= lon <= 180):
            print_error("Error 403: Longitude außerhalb des erlaubten Bereichs! 0 <= Longitude <= 180")
            return
        rtept.set("lon", str(lon))
    
    if ele is not None:
        try:
            # Editieren der elevation mit dem child element "ele", wenn es existiert
            rtept.find("{*}ele").text = str(ele)
        except Exception:
            # Erstellen des child elements "ele"
            rtept.append(lxml.etree.Element("ele"))
            rtept.find("{*}ele").text = str(ele)
    
    return input_gpx


def edit_startpoint(rte_id: int, rtept_id: int, input_gpx: gpx) -> gpx:
    """Ändert den Startpunkt einer Route zu einem bestimmten Routenpunkt.
    
    Args:
        rte_id (int): ID der Route.
        rtept_id (int): ID des neuen Startpunkts.
        input_gpx (gpx): Daten der GPX-Datei.
    
    Returns:
        gpx: Bearbeitete GPX-Daten.
    """
    
    # Abrufen der Routen aus der GPX-Datei
    rtes = _get_rtes(input_gpx)

    # Überprüfen, ob die Route und der Routenpunkt existieren
    if rte_id is None:
        print_color("Error 407: Keine Route ausgewählt!")
        return
        
    if rtept_id is None:
        print_color("Error 408: Kein Routenpunkt ausgewählt!")
        return
        
    if not (0 <= rte_id < len(rtes)) or not (0 <= rtept_id < len(rtes[rte_id][1])):
        print_color("Error 406: Route oder Routenpunkt nicht vorhanden!")
        return input_gpx

    # Neue Reihenfolge der Routenpunkte erstellen
    new_route = rtes[rte_id][1][rtept_id:] + rtes[rte_id][1][:rtept_id]

    # Aktualisieren der Routenpunkte in der GPX-Datei
    rte_element = input_gpx.etree.findall("{*}rte")[rte_id]

    # Vorherige Route löschen
    for rtept in rte_element.findall("{*}rtept"):
        rte_element.remove(rtept)

    # Einfügen der neuen Route
    for point in new_route:
        rtept = lxml.etree.Element("{*}rtept", lat=str(point[0]), lon=str(point[1]))
        if point[2] != "":
            ele = lxml.etree.Element("{*}ele")
            ele.text = str(point[2])
            rtept.append(ele)
        rte_element.append(rtept)



    return input_gpx
