""" usefull.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Verschiedene Hilsfunktionen
Autor: Leon Schuck, Pascal Köhnlein
Erstellt: 07.06.2024
"""

from colorama import Fore, Back, Style
import os

def input_type(type: str):
    """Fragt einen Input ab und versucht ihn in den angegebenen typ zu wandeln.

    Args:
        type (str): Typ in den gewandelt werden soll.

    Returns:
        _type_: Typgewandele Eingabe
    """
    while True:
        
        input_str = input()
        
        if input_str is None:
            return

        if type == int:
            try:
                return int(input_str, 10) 
            except Exception:
                print_color("Falscher Datentyp")
                continue         
        
        elif type == float:
            try:
                return float(input_str)   
            except Exception:
                print_color("Falscher Datentyp")
                continue


count = 0   # Gibt den Status von print_color an
def print_color (text):
    """Gibt den Text in gelber Schrift und abwechselnd mit schwarzem und rotem Hintergrund aus.

    Args:
        text (_type_): Text der ausgegeben werden soll
    """

    global count
    
    # Ist count gerade, wird ein schwarzer Hintergrund ausgegeben
    if count % 2 == 0 :
        print(Fore.YELLOW + Back.BLACK + text + Style.RESET_ALL)

    # Ist count ungerade, wird ein roter Hintergrund ausgegeben
    elif count % 2 == 1:
        print(Fore.YELLOW + Back.RED + text + Style.RESET_ALL)
        
    count = count + 1

def cls():
    os.system('cls' if os.name=='nt' else 'clear')