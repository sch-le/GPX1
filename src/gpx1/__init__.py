""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Pascal Köhnlein
Erstellt: 19.05.2024
"""

import sys

from gpx1.config import gpx, version
from gpx1.usefull import input_type, print_color, cls, confirm
from . import file_management
from . import parser
from . import waypoints
from . import routes
from . import tracks
from . import metadata

def main():
    """Hauptmenu, in dem die GPX-Datei geladen oder das Programm beendet werden kann.
    """
    
    ### Laden der Datei ###
    while True:    
        # Leeren der Konsole
        cls()   
        
        # Ausgabe von Optionen zum Fortfahren
        print_color(f"GPX-Editor {version}")
        print_color("Bitte wählen Sie aus folgenden Optionen aus:")
        print_color("")
        print_color("1: Auswahl einer GPX Datei")
        print_color("0: Programm Beenden ")
        
        # Abfrage der Optionen
        auswahl = input()
        
        # Programm Beenden
        if auswahl == "0":
            sys.exit()
        
        # Auswahl einer GPX Datei
        elif auswahl == "1":
            # Öffnen eines Fenster zur Auswahl der Datei
            input_gpx = file_management.open_file()

            # Falls keine Datei ausewählt wurde
            if input_gpx is None:
                print_color("Keine GPX-Datei ausgewählt!")
                confirm()
                continue
            
            # Falls Datei erfolgreich geladen wurde
            else:
                gpx_menu(input_gpx)
    
def gpx_menu(input_gpx: gpx) -> None:
    """Untermenu zum Auswählen der verschiedenen Funktionalitäten bzw. weiterer Untermenus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    #Auswahl zwischen den Funktionen
    while True:
        
        # Leeren der Konsole
        cls() 
        
        # Ausgabe Name, Beschreibung und Autor der GPX-Datei und Anzahl Waypoints, Tracks und Routs
        metadata.print_name(input_gpx)
        metadata.print_description(input_gpx)
        metadata.print_author(input_gpx)
        print_color(f"Anzahl Waypoints: {waypoints.get_count(input_gpx)}")
        print_color(f"Anzahl Tracks: {tracks.get_count(input_gpx)}")
        print_color(f"Anzahl Routes: {routes.get_count(input_gpx)}")
        print_color("")
        
        # Ausgabe von Optionen zum Fortfahren
        print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
        print_color("")
        print_color("1. Waypoints")
        print_color("2. Tracks")
        print_color("3. Routes")
        print_color("4. Metadaten")
        print_color("5. Änderungen speichern")
        print_color("0. Zurück")
        
        # Abfrage der Optionen
        auswahl = input()
        
        # Zurück ?
        if auswahl == "0":
            
            # Fragen ob wirklich ins Hauptmenu zurückgekehrt werden soll
            while True:
                
                # Leeren der Konsole
                cls()
                
                # Ausgabe von Optionen zum Fortfahren
                print_color("Achtung, alle Änderungen gehen hierdurch verloren!")
                print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
                print_color("")
                print_color("1. Abbrechen")
                print_color("0. Bestätigen")
                
                # Abfrage der Optionen
                auswahl = input()
                
                # Zurück -> Änderungen gehen verloren
                if auswahl == "0":
                    return
                
                # Abbrechen
                if auswahl == "1":
                    break
        
        # Untermenu Waypoints
        elif auswahl == "1":
           waypoint_menu(input_gpx)
           
        # Untermenu Tracks
        elif auswahl == "2":
           track_menu(input_gpx)
           
        # Untermenu Routes
        elif auswahl == "3":
           route_menu(input_gpx)
        
        # Untermenu Metadaten
        elif auswahl == "4":
           metadata_menu(input_gpx)
        
        # Änderungen speichern
        elif auswahl == "5":
            while True:
                cls()

                # Ausgabe von Optionen zum Fortfahren
                print_color("Wählen Sie einen Speicherort!")
                print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
                print_color("")
                print_color("1: Bestätigen")
                print_color("0: Abbrechen")
                
                # Abfrage der Optionen
                auswahl = input()

                # Neuen Speicherort wählen
                if auswahl == "1":
                    selected_path = file_management.save_path()
                    if selected_path:
                        # Schreiben der fertigen Datei
                        parser.write_file(input_gpx, selected_path)    
                        print_color(f"Datei wurde unter {selected_path} gespeichert!")
                        confirm()
                        break    
                    else:
                        print_color("Speichern abgebrochen.")
                        confirm()
                        break
                
                elif auswahl == "0":
                    break
            


def waypoint_menu(input_gpx: gpx) -> None:
    """Untermenu zum Auswählen der Waypoints Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    while True:
        
        # Leeren der Konsole
        cls() 
        
        # Falls keine Waypoints enthalten sind, gelangt man wieder ins vorherige Menu
        if waypoints.get_count(input_gpx) == 0:
            print_color("In Dieser Datei sind keine Waypoints enthalten.")
            confirm()
            return input_gpx
               
        # Ausgabe einer Liste mit allen Waypoints und Optionen zum fortfahren
        waypoints.print_list(input_gpx)
        print("")
        print_color("1. Bearbeiten von Waypoints")
        print_color("2. Höhendifferenz zw. zwei Waypoints berechnen")
        print_color("0. Zurück")
        
        # Abfragen der Optionen
        auswahl = input()   
        
        # Zurück
        if auswahl == "0":
            return
        
        # Bearbeiten von Waypoints
        if auswahl == "1":
            
            # Leeren der Konsole
            cls()
            
            waypoints.print_list(input_gpx) # Gibt eine Liste mit allen Waypoints aus
            print_color("")
            print_color("Geben sie bitte folgende Daten an, falls keine Änderung erwünscht ist, bestätigen sie mit Enter.")
            print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
            
            # Abfragen der zu änderenden Informationen
            print_color("ID:(Integer)")
            id = input_type(int)
            print_color("Latitute:(Float)")
            lat = input_type(float)
            print_color("Longitut:(Float)")
            lon = input_type(float)
            print_color("Elevation:(Float)")
            ele = input_type(float)
            
            # Aufrufen der Funktion zum ändern der Daten
            waypoints.edit(id, lat, lon, ele, input_gpx)

        # Höhendifferenz zw. zwei Waypoints berechnen
        if auswahl == "2":
            
            # Leeren der Konsole
            cls()
                        
            waypoints.print_list(input_gpx) # Gibt eine Liste mit allen Waypoints aus
            print_color("")
            print_color("Geben sie die IDs der Wegpunkte an")
            
            # Abfrage der Wegpunkte zwischen denen die Differenz berechnet werden soll
            print_color("ID 1:(Integer)")
            wpt_1 = input_type(int)
            print_color("ID 2:(Integer)")
            wpt_2 = input_type(int)
            
            # Aufruf der Funktion zur Berechnung der Höhendifferenz
            ele_diff = waypoints.calc_elevation(wpt_1, wpt_2, input_gpx)
            print_color(f"Höhendifferenz: {ele_diff:9.6f}")
            confirm()

def track_menu(input_gpx: gpx) -> None:
    """Untermenu zum Auswählen der Track Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """    

    while True:
        
        # Leeren der Konsole
        cls() 
         
        # Falls keine Tracks enthalten sind, gelangt man wieder ins vorherige Menu
        if tracks.get_count(input_gpx) == 0:
            print_color("In Dieser Datei sind keine Tracks enthalten.")
            confirm()
            return input_gpx
               
        # Ausgeben einer Liste mit allen Tracks und Optionen zum fortfahren                
        tracks.print_list_trks(input_gpx)    
        print_color("")
        print_color("1. Auswahl eines Tracks")
        print_color("0. Zurück")
        
        auswahl = input()   # Abfragen der Optionen
        
        # Zurück
        if auswahl == "0":
            return

        # Auswahl einer Tracks
        if auswahl == "1":
            
            # Leeren der Konsole
            cls()
            
            tracks.print_list_trks(input_gpx)    # Ausgeben einer Liste mit allen Tracks
            print_color("")
            
            # Abfrage des Tracks 
            print_color("Track-ID:(Integer)")
            trk = input_type(int)
            
            while True:
                # Leeren der Konsole
                cls()
                
                # Ausgabe einer List mit allen Tracksegmenten, bzw. Abbruch der Schleife, falls Track nicht vorhanden
                if tracks.print_list_trksegs(trk, input_gpx) is False:
                    break
                
                #Abfrage der Option zum Fortfahren
                print_color("")
                print_color("1. Auswahl eines Trackssegments")
                print_color("0. Zurück")
                auswahl = input()
                
                # Zurück
                if auswahl == "0":
                    break
                
                # Auswahl eines Tracksegments
                if auswahl == "1":
                    # Leeren der Konsole
                    cls()
                    
                    # Erneute Ausgabe der Tracksegmente
                    tracks.print_list_trksegs(trk, input_gpx)
                    
                    # Abfrage des Tracksegments 
                    print_color("")
                    print_color("Tracksegment-ID:(Integer)")
                    trkseg = input_type(int)
                    
                    while True:
                        # Leeren der Konsole
                        cls()
                        
                        # Ausgeben einer Liste mit allen Trackpoints, bzw. Abbruch der Schleife, falls Segment nicht vorhanden
                        if tracks.print_list_trkpts(trk, trkseg, input_gpx) is False:
                            break
                        
                        # Abfrage der Option zum Fortfahren
                        print_color("")
                        print_color("1. Bearbeiten eines Trackpoints")
                        print_color("0. Zurück")
                        auswahl = input()
                        
                        # Zurück
                        if auswahl == "0":
                            break
                        
                        # Auswahl eines Trackpoints
                        if auswahl == "1":
                            # Leeren der Konsole
                            cls()
                            
                            # Ausgabe einer Liste mit Trackpoints und Abfrage von Latitude, Longitude und Elevation
                            tracks.print_list_trkpts(trk, trkseg, input_gpx)
                            print_color("")
                            print_color("Geben sie bitte folgende Daten an")
                            print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                            print_color("ID:(Integer)")
                            trkpnt = input_type(int)
                            print_color("Latitute:(Float)")
                            lat = input_type(float)
                            print_color("Longitude:(Float)")
                            lon = input_type(float)
                            print_color("Elevation:(Float)")
                            ele = input_type(float)
                            
                            # Ändern des Trackpoints
                            tracks.edit(trk, trkseg, trkpnt, lat, lon, ele, input_gpx)                   

def route_menu(input_gpx: gpx) -> None:
    """Untermenu zum Auswählen der Route-Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    while True:
        
        # Leeren der Konsole
        cls()

        # Falls keine Routen enthalten sind, gelangt man wieder ins vorherige Menu
        if routes.get_count(input_gpx) == 0:
            print_color("In Dieser Datei sind keine Routen enthalten.")
            confirm()
            return input_gpx
        
        # Ausgeben einer Liste mit allen Routen und Optionen zum fortfahren                
        routes.print_rtes(input_gpx)    
        print_color("")
        print_color("1. Auswahl einer Route")
        print_color("0. Hauptmenü")

        # Abfragen der Optionen
        auswahl = input()   
        

        # Zurück
        if auswahl == "0":
            return

        # Auswahl einer Route
        elif auswahl == "1":
            
            cls()
            # Ausgeben einer Liste mit allen Routen
            routes.print_rtes(input_gpx)     
            print_color("")
            
            # Abfrage der Route 
            print_color("Route-ID:(Integer)")
            rte = input_type(int)
            
            while True:
                # Leeren der Konsole
                cls()
                
                # Ausgabe einer List mit allen Routenpunkten, bzw. Abbruch der Schleife, falls Route nicht vorhanden
                if routes.print_list_rtepts(rte, input_gpx) is False:
                    break
                
                #Abfrage der Option zum Fortfahren
                print_color("")
                print_color("1. Bearbeiten eines Routenpunktes")
                print_color("2. Bearbeiten des Startpunktes")
                print_color("0. Zurück")
                
                auswahl = input()
                
                # Zurück
                if auswahl == "0":
                    break
                
                # Auswahl eines Routenpunktes
                if auswahl == "1":
                    # Leeren der Konsole
                    cls()
                    
                    # Ausgabe einer Liste mit Routenpunkten und Abfrage von Latitude, Longitude und Elevation
                    routes.print_list_rtepts(rte, input_gpx)
                    print_color("")
                    print_color("Geben sie bitte folgende Daten an")
                    print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                    print_color("ID:(Integer)")
                    rtept = input_type(int)
                    print_color("Latitute:(Float)")
                    lat = input_type(float)
                    print_color("Longitude:(Float)")
                    lon = input_type(float)
                    print_color("Elevation:(Float)")
                    ele = input_type(float)
                    
                    # Ändern des Routenpunktes
                    routes.edit(rte, rtept, lat, lon, ele, input_gpx)

                # Ändern des Startpunktes
                if auswahl == "2":
                    # Leeren der Konsole
                    cls()

                    # Ausgabe einer Liste aller Routenpunkte
                    routes.print_list_rtepts(rte, input_gpx)
                    print_color("")
                    print_color("Bitte wählen Sie aus der Liste einen Routenpunkt als neuen Startpunkt")
                    print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                    print_color("ID:(Integer)")
                    rtept = input_type(int)

                    routes.edit_startpoint(rte, rtept, input_gpx)
                    routes.print_list_rtepts(rte, input_gpx)
                    
def metadata_menu(input_gpx: gpx) -> None:
    """Untermenü zur Auswahl der Metadata Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    while True:
        
        # Leeren der Konsole
        cls() 
        
        # Ausgabe einer Liste mit allen Metadata-Informationen und Optionen zum fortfahren
        metadata.print_name(input_gpx)
        metadata.print_description(input_gpx)
        metadata.print_author(input_gpx, True)
        
        print("")
        print_color("1. Bearbeiten des Namens")
        print_color("2. Bearbeiten der Beschreibung")
        print_color("3. Bearbeiten des Autors")
        print_color("0. Zurück")

        auswahl = input()   # Abfragen der Optionen
        
        # Zurück
        if auswahl == "0":
            return
        
        # Bearbeiten des Namens
        if auswahl == "1":
            # Leeren der Konsole
            cls()
            
            # Ausgabe des Namens der GPX-Datei
            metadata.print_name(input_gpx)
            print_color("")
            
            # Abfrage des neuen Names der GPX-Datei
            print_color("Name:(String)")
            new_name = input_type(str)
            metadata.edit_name(new_name, input_gpx)

        # Bearbeiten der Beschreibung
        if auswahl == "2":
            # Leeren der Konsole
            cls()
            
            # Ausgabe der Beschreibung der GPX-Datei
            metadata.print_description(input_gpx)
            print_color("")
            
            # Abfrage des neuen Names der GPX-Datei
            print_color("Beschreibung:(String)")
            new_desc = input_type(str)
            metadata.edit_description(new_desc, input_gpx)
        
        # Bearbeiten der Beschreibung
        if auswahl == "3":
            # Leeren der Konsole
            cls()
            
            # Ausgabe der Beschreibung der GPX-Datei
            metadata.print_author(input_gpx, True)
            print_color("")
            
            # Abfrage der neuen Autor-Informationen
            print_color("Name:(String)")
            new_name = input_type(str)
            print_color("Email:(String)")
            new_email = input_type(str)
            print_color("Link-URL:(String)")
            new_href = input_type(str)
            print_color("Link: Text:(String)")
            new_link_text = input_type(str)
            print_color("Link: Typ des Inhalts:(String)")
            new_link_type = input_type(str)
            
            # Ändern der Autor-Informationen
            metadata.edit_author(new_name, new_email, new_href, new_link_text, new_link_type, input_gpx)