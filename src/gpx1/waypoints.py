""" waypoints.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Waypoints
Autor: Leon Schuck
Erstellt: 01.06.2024
"""

from gpx1.config import gpx

def _get_wpts(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Waypoints und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    wpts = []
    
    # Suchen aller Waypoints in GPX-Datei
    for wpt in input_gpx.etree.findall("{*}wpt"):
        lat = float(wpt.get("lat"))
        lon = float(wpt.get("lon"))
        
        # Hinzufügen der optioanlen Elevation
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
    
    print("   ID   |  Latitude  |  Longitude  |  Elevation")
    print("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)
    
    # Ausgabe der Waypoint Informationen in Listenform
    for id, wpt in enumerate(wpts):
        if wpt[2] != "":
            print(f"  {id:04}  |  {wpt[0]:4.6f} |  {wpt[1]:4.6f}  | {wpt[2]:4.6f}")
        else:
            print(f"  {id:04}  |  {wpt[0]:4.6f} |  {wpt[1]:4.6f}  | {wpt[2]}")

def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Waypoints zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts
    
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
        print("Error 200: Waypoint 1 nicht vorhanden!")
        return
    
    if not (0 <= id2 <= len(wpts)):
        print("Error 201: Waypoint 2 nicht vorhanden!")
        return
    
    if wpts[id1][2] == "":
        print("Error 202: Keine Elevation Informationen zu Waypoint 1 vorhanden!")
        return
    
    if wpts[id2][2] == "":
        print("Error 203: Keine Elevation Informationen zu Waypoint 2 vorhanden!")
        return
    
    ele_diff = float(wpts[id2][2]) - float(wpts[id1][2])
    print(f"Höhendifferenz = {ele_diff}")
    
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
    
    input_gpx.etree.findall("{*}wpt")[id].set("lat", str(lat))
    input_gpx.etree.findall("{*}wpt")[id].set("lon", str(lon))
    input_gpx.etree.findall("{*}wpt")[id].find("{*}ele").text = str(ele)
    
    return input_gpx