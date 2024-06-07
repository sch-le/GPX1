""" routs.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Auslesen und Bearbeiten der Routs
Autor: Lukas Reißmann
Erstellt: 07.06.2024
"""

from gpx1.config import gpx
import lxml

def _get_wpts(input_gpx: gpx) -> list:
    """Erstellt eine Liste mit allen Waypoints (Routenpunkte) und der dazugehörigen Latitude, Longitude und optionalen Elevation

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        list: Liste mit Latitude, Longitude, Elevation
    """
    
    wpts = []
    
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
        
            wpts.append([lat, lon, ele])
    
    return wpts

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

