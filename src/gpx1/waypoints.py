""" waypoints.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen, Bearbeiten und Berechnen von Waypoint-Informationen
Autor: Leon Schuck
Erstellt: 01.06.2024
"""

from gpx1.config import gpx
from gpx1.usefull import print_color, print_error
import lxml

def _get_wpts(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Waypoints und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    """Liste mit allen Waypoints und dazugehöriger Latitude, Longitude und Elevation
    Format: [   [wpt1_lat, wpt1_lon, wpt1_ele],
                [wpt2_lat, wpt2_lon, wpt2_ele],
                .... 
                [wptn_lat, wptn_lon, wptn_ele],
            ]
    """
    wpts = []   
    
    # Suchen aller Waypoints in GPX-Datei
    for wpt in input_gpx.etree.findall("{*}wpt"):   # Loop über Liste aller "wpt" Elemente
        
        # Auslesen der Latitude und Logitude aus den Child-Elementen "lat" und "lon"
        lat = float(wpt.get("lat"))
        lon = float(wpt.get("lon"))    
        
        # Hinzufügen der optioanlen Elevation aus Child-Element "ele", falls dieses vorhanden ist
        ele = ""
        if wpt.find("{*}ele") is not None:
            ele = float(wpt.find("{*}ele").text)
        
        # Hinzufügen der Daten zur Liste
        wpts.append([lat, lon, ele])
    
    return wpts

def print_list(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Waypoints und der dazugehörigen Latitude, Longitude und optinalen Elevation aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)
        
    print_color("   ID   |  Latitude  |  Longitude  |  Elevation  ")
    print_color("--------|------------|-------------|-------------")
    
    # Ausgabe der Waypoint Informationen in Listenform
    for id, wpt in enumerate(wpts):
        # Falls optionale Elevation-Information enthalten ist, wird diese mit ausgegeben
        if wpt[2] != "":
            print_color(f"  {id: 4}  | {wpt[0]: 10.6f} | {wpt[1]: 11.6f} |  {wpt[2]: 9.3f}  " ) 
        else:                            
            print_color(f"  {id: 4}  | {wpt[0]: 10.6f} | {wpt[1]: 11.6f} |             ")

def get_count(input_gpx: gpx) -> int: 
    """Gibt die Anzahl der in der Datei vorkommenden Waypoints zurück

    Args:
        input_gpx (gpx): Daten der GPX-Datei
        
    Returns:
        int: Amzahl der Waypoints
    """
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)
    
    # Gibt die Anzahl der Elemente (Waypoints) zurück
    return len(wpts)

def calc_elevation(id1: int, id2: int, input_gpx) -> float:
    """Gibt den Höhenunterschied zwischen zwei Waypoints zurück

    Args:
        id1 (int): ID des ersten Waypoints
        id2 (int): ID des zweiten Waypoints

    Returns:
        float: Höhendifferenz
    """
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)
    
    # Überprüfung ob Waypoint 1 existiert
    if not (0 <= id1 <= len(wpts)):
        print_error("Error 200: Waypoint 1 nicht vorhanden!")
        return

    # Überprüfung ob Waypoint 1 existiert
    if not (0 <= id2 <= len(wpts)):
        print_error("Error 201: Waypoint 2 nicht vorhanden!")
        return
    
    # Überprüfung ob in Waypoint 1 die Elevation gespeichert ist (diese ist optional)
    if wpts[id1][2] == "":
        print_error("Error 202: Keine Elevation Informationen zu Waypoint 1 vorhanden!")
        return
    
    # Überprüfung ob in Waypoint 2 die Elevation gespeichert ist (diese ist optional)
    if wpts[id2][2] == "":
        print_error("Error 203: Keine Elevation Informationen zu Waypoint 2 vorhanden!")
        return
    
    # Berechnung und Rückgabe der Höhendifferenz
    return(float(wpts[id2][2]) - float(wpts[id1][2]))
    
def edit(wpt_id: int, lat: float, lon: float, ele: float, input_gpx: gpx) -> None:
    """Ändert die Latitude, Longitude und Elevation eines gegebenen Waypoints
 
    Args:
        id (int): ID des zu bearbeitenden Waypoints
        lat (float): Neue Latitude / None: keine Änderung
        lon (float): Neue Longitude / None: keine Änderung
        ele (float): Neue Elevation / None: keine Änderung
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    # Erstellen einer Liste mit allen Waypoints
    wpts = _get_wpts(input_gpx)

    # Überprüfung ob Waypoint existiert
    if wpt_id is None:
        print_error("Error 206: Kein Waypoint ausgewählt!")
        return
    if not (0 <= wpt_id < len(wpts)):
        print_error("Error 204: Waypoint nicht vorhanden!")
        return

    # Suchen des bestimmten Elements "wpt"
    wpt = input_gpx.etree.findall("{*}wpt")[wpt_id]
    
    # Ändern der Latitude und Longitude, über die Child-Elemente "lat" und "lon"
    if lat is not None:
        # Bereichsüberprüfung der Latitude
        if not (-90 <= lat <= 90):
            print_error("Error 205: Latitude außerhalb des erlaubten Bereichs!  -90 <= Latitude <= 90")
            return
        wpt.set("lat", str(lat))
        
    if lon is not None:
        # Bereichsüberprüfung der Longitude
        if not (-180 <= lon <= 180):
            print_error("Error 206: Latitude außerhalb des erlaubten Bereichs! -180 <= Longitude <= 180")
            return
        wpt.set("lon", str(lon))
    
    # Ändern bzw. Erstellen des Child-Elements für Elevation
    if ele is not None:
        try:
            # Ändern der Elevation über Child-Element "ele", falls dieses vorhanden ist
            wpt.find("{*}ele").text = str(ele)
        except Exception:
            # Erstellen des Child-Elements "ele"
            wpt.append(lxml.etree.Element("ele"))
            wpt.find("{*}ele").text = str(ele)