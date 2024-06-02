""" __init__.py

Beschreibung: Editor, mit dem GPX-Dateien bearbeitet werden können
Autor: Pascal Köhnlein
Erstellt: 19.05.2024
"""

#Globale Variablen
count = 0

#Funktionen
#Erstellen der Farbwechsel Funktion
def PrintColor (Text):
    #Hier wird mit Globalen Variablen gearbeitet
    global count
    #Ist count gerade dann wird ein schwarzer Hintergrund ausgegeben
    if count % 2 == 0 :
        print (Fore.YELLOW + Back.BLACK + Text + Style.RESET_ALL)

    #Ist count ungerade dann wird ein roter Hintergrund ausgegeben
    elif count % 2 == 1:
        print(Fore.YELLOW + Back.RED + Text + Style.RESET_ALL)
    count = count + 1

#Einführen von Colorama
from colorama import init, Fore, Back, Style

#Deklarieren von Laufvariablen
Startabfrage = 0
Funktionauswahl = 0

#Start des Programmes
PrintColor("Willkommen im GPX-Editor")
PrintColor("Bitte wählen Sie aus folgenden Optionen aus:")

#Eingangs abfrage: Auswahl einer Datei
while True:
    PrintColor("0: Programm Beenden ")
    PrintColor("1: Auswahl einer GPX Datei")
    Startabfrage = input()

 #Soll Programm beendet werden?
    PrintColor(Startabfrage)
    if Startabfrage == "0" or Startabfrage == "1":
        PrintColor("Break")
        break
        
    else:
        PrintColor("Wählen sie bitte nur zwischen 0 & 1")

    #Auswahl einer Datei treffen
while Startabfrage == "1": 
    PrintColor("Wählen Sie bitte die gewünschte Datei aus")
    PrintColor("Hier wird gepasst")
    # Passing einfügen

    #Auswahl zwischen den Funktionen
    while True:
        PrintColor("Wählen sie bitte zwischen folgenden Optionen aus:")
        PrintColor("0: Programm beenden")
        PrintColor("1: Bearbeiten von Tracks")
        PrintColor("2: Bearbeiten von Waypoints")
        PrintColor("3: Bearbeiten von Routs")
        PrintColor("4: Höhen Differenz zw. zwei Waypoints berechnen")
        PrintColor("5: Anzahl der Waypoints anzeigen")
        Funktionauswahl = input()
        #Beenden des Programms
        if Funktionauswahl == "0":
            PrintColor("Break in der Funktionsauswahl")
            Startabfrage = "0"
            break

            #Funktion Track wird aufgerufen
        elif Funktionauswahl == "1":
            PrintColor("Hier werden die Tracks bearbeitet")
            #Funktion Track einfügen

            #Funktion Waypoint wird aufgerufen
        elif Funktionauswahl == "2":
            PrintColor("Hier werden die Waypoints bearbeitet")
            #Funktion Waypoints einfügen

            #Funktion Routs wird aufgerufen
        elif Funktionauswahl == "3":
            PrintColor("Hier werden die Routs bearbeitet")
            #Funktion Routs einfügen

            #Funktion berrechnung Höhendifferenz wird aufgerufen
        elif Funktionauswahl == "4":
            PrintColor("Hier werden die Höhen diff berechnet ")
            #Funktion Höhen diff berechnen einfügen

            #Funktion Anzahl Waypoints wird aufgerufen
        elif Funktionauswahl == "5":
            PrintColor("Hier werden die Anz. Waypoints angezeigt")
            #Funktion Anz.Waypoints einfügen

    #Programm wird beendet
    if Startabfrage == "0":
    
        break