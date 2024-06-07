""" routs.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Routs
Autor: Lukas Reißmann
Erstellt: 07.06.2024
"""

from gpx1.config import gpx
import lxml

def _get_wpts(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Routenpunkte und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    rpts = []
    
    # Suchen aller Routenpunkte (rtept) in der GPX-Datei
    
    # Loop über alle "rte" Elemente
    for rte in input_gpx.etree.findall("{*}rte"):  
        # Loop über alle "rtept" Elemente innerhalb einer "rte"
        for rtept in rte.findall("{*}rtept"):   
        
            # Auslesen der Latitude und Logitude aus den Attributen "lat" und "lon"
            lat = float(rtept.get("lat"))
            lon = float(rtept.get("lon"))    
        
            # Hinzufügen der optionalen Elevation als Child-Element "ele", falls dieses vorhanden ist
            ele = ""
            if rtept.find("{*}ele") is not None:
                ele = float(rtept.find("{*}ele").text)
        
            rpts.append([lat, lon, ele])
    
    return rpts

def print_list(input_gpx: gpx) -> None:
    """Gibt eine Liste mit allen Routenpunkte und der dazugehörigen Latitude Longitude und optinalen Elevation aus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    print("   ID   |  Latitude  |  Longitude  |  Elevation")
    print("--------|------------|-------------|-------------")
    
    # Erstellen einer Liste mit allen Routenpunkt
    rpts = _get_wpts(input_gpx)
    
    # Ausgabe der Routenpunkt Informationen in Listenform
    for id, rpt in enumerate(rpts):
        if rpt[2] != "":
            print(f"  {id:04}  |  {rpt[0]:9.6f} |  {rpt[1]:9.6f}  | {rpt[2]:9.6f}")
        else:
            print(f"  {id:04}  |  {rpt[0]:9.6f} |  {rpt[1]:9.6f}  | {rpt[2]} ")


def get_count(input_gpx: gpx) -> int:
    """Gibt die Anzahl der in der Datei vorkommenden Routenpunkte zurück

    Args:
        input_gpx (gpx): _description_
    """
    
    rpts = _get_wpts
    
    return len(rpts)


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
    
    rpts = _get_wpts(input_gpx)

    if not (0 <= id <= len(rpts)):
        print("Error 204: Routenpunkt nicht vorhanden!")
        return
    
    # Suchen des bestimmten Elements "wpt"
    rpt = input_gpx.etree.findall("{*}rtept")[id]
    
    # Ändern der Latitude und Longitude, über die Child-Elemente "lat" und "lon"
    if lat is not None:
        rpt.set("lat", str(lat))
        
    if lon is not None:
        rpt.set("lon", str(lon))
    
    if ele is not None:
        try:
            # Ändern der Elevation über Child-Element "ele", falls dieses vorhanden ist
            rpt.find("{*}ele").text = str(ele)
        except Exception:
            # Erstellen des Child-Elements "ele"
            rpt.append(lxml.etree.Element("ele"))
            rpt.find("{*}ele").text = str(ele)
    
    print_list(input_gpx)
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
    
    # Das erste "rtept"-Element auswählen, um den Startpunkt zu ändern
    startpoint = input_gpx.etree.find("{*}rte/{*}rtept")
    
    # Überprüfen, ob ein Startpunkt vorhanden ist
    if startpoint is None:
        print("Error: Kein Startpunkt vorhanden!")
        return input_gpx
    
    # Ändern der Breiten- und Längengrade des Startpunkts
    startpoint.set("lat", str(lat))
    startpoint.set("lon", str(lon))
    
    # Ändern der Elevation, falls vorhanden, oder erstellen, falls nicht vorhanden
    ele_element = startpoint.find("{*}ele")
    if ele_element is not None:
        ele_element.text = str(ele)
    else:
        ele_element = lxml.etree.Element("ele")
        ele_element.text = str(ele)
        startpoint.append(ele_element)
    
    # Rückgabe der bearbeiteten GPX-Daten
    return input_gpx

