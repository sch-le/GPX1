"""
...
"""
Startabfrage = 0
Funktionauswahl = 0

print("Willkommen im GPX-Editor\n")
print("Bitte wählen Sie aus folgenden Optionen aus:")

while True:
    Startabfrage = input("0: Programm Beenden \n1: Auswahl einer GPX Datei\n")

 
    print(Startabfrage)
    if Startabfrage == "0" or Startabfrage == "1":
        print("Break")
        break
        
    else:
        print("Wählen sie bitte nur zwischen 0 & 1")

while Startabfrage == "1": 
    print("Wählen Sie bitte die gewünschte Datei aus")
    print("Hier wird gepasst")
    # Passing einfügen

    while True:
        print("Wählen sie bitte zwischen folgenden Optionen aus:")
        Funktionauswahl = input("0: Programm beenden\n1: Bearbeiten von Tracks\n2: Bearbeiten von Waypoints\n3: Bearbeiten von Routs\n4: Höhen Differenz zw. zwei Waypoints berechnen\n5: Anzahl der Waypoints anzeigen\n ")

        if Funktionauswahl == "0":
            print("Break in der Funktionsauswahl")
            Startabfrage = "0"
            break

        elif Funktionauswahl == "1":
            print("Hier werden die Tracks bearbeitet")
            #Funktion Track einfügen

        elif Funktionauswahl == "2":
            print("Hier werden die Waypoints bearbeitet")
            #Funktion Waypoints einfügen

        elif Funktionauswahl == "3":
            print("Hier werden die Routs bearbeitet")
            #Funktion Routs einfügen
        
        elif Funktionauswahl == "4":
            print("Hier werden die Höhen diff berechnet ")
            #Funktion Höhen diff berechnen einfügen

        elif Funktionauswahl == "5":
            print("Hier werden die Anz. Waypoints angezeigt")
            #Funktion Anz.Waypoints einfügen

    if Startabfrage == "0":
    
        break