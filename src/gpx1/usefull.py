""" usefull.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Verschiedene Hilfsfunktionen
Autor: Leon Schuck, Pascal Köhnlein
Erstellt: 07.06.2024
"""

from colorama import Fore, Back, Style
import os
import sys

def input_type(type: str) -> any:
    """Fragt einen Input ab und versucht ihn in den angegebenen typ zu wandeln.

    Args:
        type (str): Typ in den gewandelt werden soll.

    Returns:
        any: Typgewandele Eingabe
    """
    
    while True:
        # Einlesen des Inputs
        input_str = input()
              
        # Falls Input None ist wird None zurückgegeben
        if input_str == "":
            return None

        # Falls Input vom Typ int sein soll
        if type == int:
            try:
                return int(input_str, 10) 
            except Exception:
                print_color("Falscher Datentyp!")
                continue         
        
        # Falls Input vom Tpy float sein soll
        elif type == float:
            try:
                return float(input_str)   
            except Exception:
                print_color("Falscher Datentyp!")
                continue
            
        # Falls Input com Tpy str sein soll
        if type == str:
            return input_str
            
count: int = 0   # Gibt den Status von print_color an
def print_color(text: str):
    """Gibt den Text in gelber Schrift und abwechselnd mit schwarzem und rotem Hintergrund aus.

    Args:
        text (str): Text der ausgegeben werden soll
    """

    global count
    
    # Ist count gerade, wird ein schwarzer Hintergrund ausgegeben
    if count % 2 == 0 :
        print(Fore.YELLOW + Back.BLACK + text + Style.RESET_ALL)

    # Ist count ungerade, wird ein roter Hintergrund ausgegeben
    elif count % 2 == 1:
        print(Fore.YELLOW + Back.RED + text + Style.RESET_ALL)
        
    count = count + 1

def print_error(text: str, confirm_error: bool =True, exit_error: bool =False):
    """Gibt eine Fehlermeldung aus, wartet auf Bestätigung und beendet dann ggf. das gesamte Programm.

    Args:
        text (str): Fehlermeldung
        confirm (bool, optional): Gibt an ob auf Bestätigung durch Tastendruck gewartet werden soll. Defaults to True.
        exit (bool, optional): Gibt an ob Programm nach Ausgabe der Fehlermeldung beendet werden soll. Defaults to False.
    """
    
    # Ausgabe der Fehlermeldung
    print_color(text)
    
    # Wartet auf Tasteneingabe, falls gefordert
    if confirm_error is True:
        confirm()
    
    # Beendet das Programm, falls gefordert, wartet hier immer auf Bestätigung
    if exit_error is True:
        if confirm_error is False:
            confirm()
        sys.exit()

def confirm():
    """Gibt Text mit Aufforderung zur Bestätigung aus und wartet dann auf Tastendruck.
    """
    
    print_color("Bestätigen Sie mit beliebiger Taste.")
    input()

def cls():
    """Leert den Inhalt der Konsole.
    """
    
    # Bei Linux und Mac über den Befehl "clear", bei Windows über "cls"
    os.system('cls' if os.name=='nt' else 'clear')