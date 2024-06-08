""" waypoints.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Waypoints
Autor: Leon Schuck
Erstellt: 01.06.2024
"""

from gpx1.config import gpx
from gpx1.usefull import print_color
import lxml

def _get_wpts(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Waypoints und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    wpts = []
    
    # Suchen aller Waypoints in GPX-Datei
    for wpt in input_gpx.etree.findall("{*}wpt"):   # Loop über alle "wpt" Elemente
        
        # Auslesen der Latitude und Logitude aus den Child-Elementen "lat" und "lon"
        lat = float(wpt.get("lat"))
        lon = float(wpt.get("lon"))    
        
        # Hinzufügen der optioanlen Elevation as Child-Element "ele", falls dieses vorhanden ist
        ele = ""
        if wpt.find("{*}ele") is not None:
            ele = float(wpt.find("{*}ele").text)
        
        wpts.append([lat, lon, ele])
    
    return wpts

def print_list(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Waypoints und der dazugehörigen Latitude Longitude und optinalen Elevation aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation")
    print_color("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)
    
    # Ausgabe der Waypoint Informationen in Listenform
    for id, wpt in enumerate(wpts):
        if wpt[2] != "":
            print_color(f"  {id:04}  |  {wpt[0]:9.6f} |  {wpt[1]:9.6f}  | {wpt[2]:9.6f}")
        else:
            print_color(f"  {id:04}  |  {wpt[0]:9.6f} |  {wpt[1]:9.6f}  | {wpt[2]} ")

def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Waypoints zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    wpts = _get_wpts(input_gpx)
    
    return len(wpts)

def calc_elevation(id1: int, id2: int, input_gpx) -> float:
    """Gibt den Höhenunterschied zwischen zwei Waypoints zurück

    Args:
        id1 (int): ID des ersten Waypoints
        id2 (int): ID des zweiten Waypoints

    Returns:
        float: Höhendifferenz
    """
    
    wpts = _get_wpts(input_gpx)
    
    if not (0 <= id1 <= len(wpts)):
        print_color("Error 200: Waypoint 1 nicht vorhanden!")
        return
    
    if not (0 <= id2 <= len(wpts)):
        print_color("Error 201: Waypoint 2 nicht vorhanden!")
        return
    
    if wpts[id1][2] == "":
        print_color("Error 202: Keine Elevation Informationen zu Waypoint 1 vorhanden!")
        return
    
    if wpts[id2][2] == "":
        print_color("Error 203: Keine Elevation Informationen zu Waypoint 2 vorhanden!")
        return
    
    ele_diff = float(wpts[id2][2]) - float(wpts[id1][2])
    return(ele_diff)
    
def edit(id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> gpx:
    """Ändert die Latitude, Longitude und Elevation eines gegebenen Waypoints
 
    Args:
        id (int): ID des zu bearbeitenden Waypoints
        lat (float): Latitude
        lon (float): Longitude
        ele (float): Elevation
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        gpx: Bearbeitete GPX-Daten
    """
    
    wpts = _get_wpts(input_gpx)

    if not (0 <= id <= len(wpts)):
        print_color("Error 204: Waypoint nicht vorhanden!")
        return
    
    # Suchen des bestimmten Elements "wpt"
    wpt = input_gpx.etree.findall("{*}wpt")[id]
    
    # Ändern der Latitude und Longitude, über die Child-Elemente "lat" und "lon"
    if lat is not None:
        wpt.set("lat", str(lat))
        
    if lon is not None:
        wpt.set("lon", str(lon))
    
    if ele is not None:
        try:
            # Ändern der Elevation über Child-Element "ele", falls dieses vorhanden ist
            wpt.find("{*}ele").text = str(ele)
        except Exception:
            # Erstellen des Child-Elements "ele"
            wpt.append(lxml.etree.Element("ele"))
            wpt.find("{*}ele").text = str(ele)
    
    print_list(input_gpx)
    return input_gpx