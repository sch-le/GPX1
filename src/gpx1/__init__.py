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
from . import routs
from . import tracks



def main():
    """Hauptmenu, in dem die GPX-Datei geladen oder das Programm beendet werden kann.
    """
    
    ### Laden der Datei ###
    while True:    
        # Leeren der Konsole
        cls()   
        
        print_color("GPX-Editor {version}")
        print_color("Bitte wählen Sie aus folgenden Optionen aus:")
        print_color("")
        print_color("1: Auswahl einer GPX Datei")
        print_color("0: Programm Beenden ")
        
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
    
def gpx_menu(input_gpx: gpx):
    """Untermenu zum Auswählen der verschiedenen Funktionalitäten bzw. weiterer Untermenus

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    #Auswahl zwischen den Funktionen
    while True:
        
        # Leeren der Konsole
        cls() 
        
        print_color(f"Anzahl Waypoints: {waypoints.get_count(input_gpx)}")
        print_color(f"Anzahl Tracks: {tracks.get_count(input_gpx)}")
        print_color(f"Anzahl Routs: {routs.get_count(input_gpx)}")
        print_color("")
        
        print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
        print_color("")
        
        print_color("1: Waypoints")
        print_color("2: Tracks")
        print_color("3: Routs")
        print_color("4: Metadaten")
        print_color("5: Änderungen speichern")
        print_color("0: Zurück")
        
        auswahl = input()
        
        # Zurück ?
        if auswahl == "0":
            
            # Fragen ob wirklich ins Hauptmenu zurückgekehrt werden soll
            while True:
                
                # Leeren der Konsole
                cls()
                
                print_color("Achtung, alle Änderungen gehen hierdurch verloren!")
                print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
                print_color("")
                print_color("1: Abbrechen")
                print_color("0: Bestätigen")
                
                auswahl = input()
                
                # Zurück -> Änderungen gehen verloren
                if auswahl == "0":
                    return()
                
                # Abbrechen
                if auswahl == "1":
                    break
        
        # Untermenu Waypoints
        elif auswahl == "1":
           input_gpx = waypoint_menu(input_gpx)
           
        # Untermenu Tracks
        elif auswahl == "2":
           input_gpx = track_menu(input_gpx)
           
        # Untermenu Routs
        elif auswahl == "3":
           input_gpx = rout_menu(input_gpx)
        
        # Untermenu Metadaten
        elif auswahl == "4":
           ...
        
        # Änderungen speichern
        elif auswahl == "5":
            parser.write_file(input_gpx)    # Schreiben der fertigen Datei
            print_color("Datei wurde unter ... gespeichert!")
            confirm()

def waypoint_menu(input_gpx: gpx):
    """_summary_

    Args:
        input_gpx (gpx): _description_
    """
    
    while True:
        
        # Leeren der Konsole
        cls() 
                        
        waypoints.print_list(input_gpx)
        print("")
        print_color("1. Bearbeiten von Waypoints")
        print_color("2. Höhendifferenz zw. zwei Waypoints berechnen")
        print_color("0. Zurück")
        
        auswahl = input()
        
        # Zurück
        if auswahl == "0":
            return input_gpx
        
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
            print_color("longitut:(Float)")
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

def track_menu(input_gpx: gpx):
    """Untermenu zum Auswählen der Track Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    while True:
        
        # Leeren der Konsole
        cls() 
                        
        tracks.print_list_trks(input_gpx)    # Ausgeben einer Liste mit allen Tracks
        print_color("")
        
        print_color("1. Auswahl eines Tracks")
        print_color("0. Zurück")
        
        auswahl = input()
        
        # Zurück
        if auswahl == "0":
            return input_gpx

        # Auswahl einer Tracks
        if auswahl == "1":
            
            # Leeren der Konsole
            cls()
            
            tracks.print_list_trks(input_gpx)    # Ausgeben einer Liste mit allen Tracks
            print_color("")
            
            # Abfrage des Tracks 
            print_color("ID:(Integer)")
            trk = input_type(int)
            
            while True:
                # Leeren der Konsole
                cls()
                
                tracks.print_list_trksegs(trk, input_gpx)    # Ausgabe einer Liste mit allen Tracksegmenten
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
                    
                    tracks.print_list_trksegs(trk, input_gpx)    # Ausgabe einer Liste mit allen Tracksegmenten
                    print_color("")
                    
                    # Abfrage des Tracksegments 
                    print_color("ID:(Integer)")
                    trkseg = input_type(int)
                    
                    while True:
                        # Leeren der Konsole
                        cls()
                        
                        tracks.print_list_trkpts(trk, trkseg, input_gpx) # Ausgeben einer Liste mit allen Trackpoints
                        print_color("")
                        
                        print_color("1. Bearbeiten eines Trackpoints")
                        print_color("0. Zurück")
                        
                        auswahl = input()
                        
                        # Zurück
                        if auswahl == "0":
                            break
                        
                        # Auswahl eines Trackpoints
                        if auswahl == "1":
                            cls()
                            tracks.print_list_trkpts(trk, trkseg, input_gpx)
                            print_color("")
                            print_color("Geben sie bitte folgende Daten an")
                            print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                            print_color("ID:(Integer)")
                            trkpnt = input_type(int)
                            print_color("Latitute:(Float)")
                            lat = input_type(float)
                            print_color("longitut:(Float)")
                            lon = input_type(float)
                            print_color("Elevation:(Float)")
                            ele = input_type(float)
                            tracks.edit(trk, trkseg, trkpnt, lat, lon, ele, input_gpx)                   

def rout_menu(input_gpx: gpx):
    """Untermenu zum Auswählen der Rout-Funktionen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    while True:
        
        # Leeren der Konsole
        cls()
        
        routs.print_rtes(input_gpx)
        print_color("")
        print_color("1. Auswahl einer Route")                    
        print_color("0. Hauptmenü")
        
        auswahl = input()

        # Zurück
        if auswahl == "0":
            return input_gpx

        # Auswahl einer Route
        elif auswahl == "1":
            cls()
            routs.print_rtes(input_gpx)
            print_color("[id] Wählen sie eine der aufgelisteten Routen!")
            route_id = input_type(int)
            rtepts = routs._get_rtepts(route_id, input_gpx)
                        
            print_color("1. Bearbeiten von Routenpunkten")
            print_color("2. Bearbeiten von Startpunkt")                    
            print_color("0. Hauptmenü")
            
            auswahl = input()

            if auswahl == "0":
                break
                       
            elif auswahl == "1":
                cls()
                routs.print_list_rtepts(route_id,input_gpx)
            
                print_color("\nGeben sie bitte folgende Daten an")
                print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
            
                # Abfragen der Routepoint Informationen
                print_color("ID:(Integer)")
                rpt_id = input_type(int)
                print_color("Latitute:(Float)")
                lat = input_type(float)
                print_color("longitut:(Float)")
                lon = input_type(float)
                print_color("Elevation:(Float)")
                ele = input_type(float)

                routs.edit(rpt_id, lat, lon, ele, input_gpx)
            
            # Auswah
            elif auswahl == "2":
                cls()

                routs.print_startpoint(route_id, input_gpx)
                
                print_color("\nGeben sie bitte folgende Daten an")
                print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
            
                # Abfragen der Routepoint Informationen
                print_color("ID:(Integer)")
                rpt_id = input_type(int)
                print_color("Latitute:(Float)")
                lat = input_type(float)
                print_color("longitut:(Float)")
                lon = input_type(float)
                print_color("Elevation:(Float)")
                ele = input_type(float)
                
                routs.edit_startpoint(lat, lon, ele, input_gpx)
                
            