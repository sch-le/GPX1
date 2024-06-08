""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Pascal Köhnlein
Erstellt: 19.05.2024
"""

import sys

#from . import parser
from . import waypoints
from . import routs
from . import track
from . import file_management
from gpx1.usefull import input_type, print_color, cls



def main():
    
    #Deklarieren von Laufvariablen
    Startabfrage = 0
    Funktionauswahl = 0
    Modulabfrage = 0

    #Start des Programmes
    print_color("Willkommen im GPX-Editor")
    print_color("Bitte wählen Sie aus folgenden Optionen aus:")

    #Eingangs abfrage: Auswahl einer Datei
    while True:
        print_color("0: Programm Beenden ")
        print_color("1: Auswahl einer GPX Datei")
        Startabfrage = input()

    #Soll Programm beendet werden?
        if Startabfrage == "0" or Startabfrage == "1":
            break
            
        else:
            print_color("Wählen sie bitte nur zwischen 0 & 1")

        #Auswahl einer Datei treffen
    while Startabfrage == "1": 
        print_color("Wählen Sie bitte die gewünschte Datei aus")
        input_gpx = file_management.open_file()

        print_color(f"Anzahl Waypoints: {waypoints.get_count(input_gpx)}")
        print_color(f"Anzahl Tracks: {track.get_count(input_gpx)}")
        print_color(f"Anzahl Routs: {routs.get_count(input_gpx)}")

        #Auswahl zwischen den Funktionen
        while True:
            print_color("Wählen sie bitte zwischen folgenden Optionen aus:")
            print_color("0: Programm beenden")
            print_color("1: Waypoints")
            print_color("2: Tracks")
            print_color("3: Routs")
            print_color("4: Metadaten")
            Modulabfrage = input()


            #Beenden des Programms
            if Modulabfrage == "0":
                Startabfrage = "0"
                break
        
            # Untermenu Waypoints    
            elif Modulabfrage == "1":
    
                while True:
                    cls()
                    
                    waypoints.print_list(input_gpx)
                    print_color("\n1. Bearbeiten von Waypoints")
                    print_color("2. Höhendifferenz zw. zwei Waypoints berechnen")
                    print_color("0. Hauptmenü")
                    
                    Funktionauswahl = input()

                    if Funktionauswahl == "1":
                        cls()
                        
                        waypoints.print_list(input_gpx)
                        print_color("\nGeben sie bitte folgende Daten an")
                        print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                        
                        # Abfragen der Waypoint Informationen
                        print_color("ID:(Integer)")
                        id = input_type(int)
                        print_color("Latitute:(Float)")
                        lat = input_type(float)
                        print_color("longitut:(Float)")
                        lon = input_type(float)
                        print_color("Elevation:(Float)")
                        ele = input_type(float)
                        
                        waypoints.edit(id, lat, lon, ele, input_gpx)
                    
                    elif Funktionauswahl == "2":
                        cls()
                        
                        waypoints.print_list(input_gpx)
                        print_color("\nGeben sie die IDs der Wegpunkte an")
                        print_color("ID 1:(Integer)")
                        id1 = input_type(int)
                        print_color("ID 2:(Integer)")
                        id2 = input_type(int)
                        ele_diff = waypoints.calc_elevation(id1, id2, input_gpx)
                        print_color(f"Höhendifferenz: {ele_diff:9.6f}")
                        input()

                    elif Funktionauswahl == "0":
                        cls()
                        break

                    else:
                        print_color("Unzulässige Eingabe")
            
            # Untermenu Tracks    
            elif Modulabfrage == "2":

                while True:
                    cls()
                    track.print_list_trks(input_gpx)
                    print_color("")
                    print_color("1. Auswahl eines Tracks")
                    print_color("0. Hauptmenü")

                    Funktionauswahl = input()

                    if Funktionauswahl == "1":
                        cls()
                        print_color("ID:(Integer)")
                        id = input_type(int)
                        track.print_list_trksegs(id, input_gpx)  
                        print_color("")
                        print_color("1. Auswahl eines Trackssegments")
                        print_color("0. Hauptmenü")

                        Funktionauswahl = input()
                        
                        if Funktionauswahl == "1":
                            ...
                            
                    #if Funktionauswahl == "1":
                    #    print_color("Geben sie bitte folgende Daten an")
                    #    print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                    #    print_color("ID:(Integer)")
                    #    id = input_type(int)
                    #    print_color("Latitute:(Float)")
                    #    lat = input_type(float)
                    #    print_color("longitut:(Float)")
                    #    lon = input_type(float)
                    #    print_color("Elevation:(Float)")
                    #    ele = input_type(float)
                    #    track.edit(id, lat, lon, ele, input_gpx)

                    elif Funktionauswahl == "0":
                        break

                    else:
                        print_color("Unzulässige Eingabe")

            # Untermenu Routen
            elif Modulabfrage == "3":
                while True:
                    cls()
                    routs.print_rtes(input_gpx)
                    print_color("")
                    print_color("1. Auswahl einer Route")                    
                    print_color("0. Hauptmenü")
                    
                    Funktionauswahl = input()

                    if Funktionauswahl == "1":
                        cls()
                        routs.print_rtes(input_gpx)
                        print_color("[id] Wählen sie einer der Aufgelisteten Routen!")
                        id = input_type(int)
                        routs._get_rtepts(id, input_gpx)
                                           
                        print_color("1. Bearbeiten von Routenpunkten")
                        print_color("2. Bearbeiten von Startpunkt")                    
                        print_color("0. Hauptmenü")
                        id = input_type(int)
                        
                        Funktionauswahl = input()

                        if Funktionauswahl == "1":
                            routs.print_list_rtepts(input_gpx)
                        
                            print_color("\nGeben sie bitte folgende Daten an")
                            print_color("Bitte beachten sie den geforderten Datentyp in der Klammer")
                        
                            # Abfragen der Routepoint Informationen
                            print_color("ID:(Integer)")
                            id = input_type(int)
                            print_color("Latitute:(Float)")
                            lat = input_type(float)
                            print_color("longitut:(Float)")
                            lon = input_type(float)
                            print_color("Elevation:(Float)")
                            ele = input_type(float)

                            routs.edit(id, lat, lon, ele, input_gpx)
                        
                        elif Funktionauswahl == "2":
                            
                            routs.edit_startpoint(input_gpx)
                        
                        elif Funktionauswahl == "0":
                            break
            
                           
            elif Modulabfrage == "4":
                print_color("Name:")
                print_color("Beschreibung")
                print_color("Autor")

                while True:
                    print_color("1. Bearbeiten der Metadaten")
                    print_color("0. Hauptmenü")
                    Funktionauswahl = input()
                    if Funktionauswahl == "1":
                        ...
                        #Funktion einfügen
                    elif Funktionauswahl == "0":
        
                        break

                    else:
                        print_color("Unzulässige Eingabe")

        #Programm wird beendet
        if Startabfrage == "0":
        
            break