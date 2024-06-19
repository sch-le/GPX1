""" waypoints.py

(c) PaFeLe²KyLuKa-Industries

Beschreibung: Funktionen zum Ausgeben und Bearbeiten von Metadata-Informationen
Autor: Leon Schuck
Erstellt: 18.06.2024
"""

import lxml
import re
from dataclasses import dataclass

from gpx1.config import gpx
from gpx1.usefull import print_color, print_error

@dataclass
class AuthorInfo:
    """Datenklasse zum Speichern der Author-Informationen
    """
    name: str
    email_id: str
    email_domain: str
    href: str
    link_text: str
    link_type:str
    

def _get_name(input_gpx: gpx) -> str:
    """Sucht den in Metadata definierten Namen der GPX-Datei und gibt diesen zurück.

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        str: Name der GPX Datei
    """
   
    # Platzhalter für Namen, falls Element leer ist
    name = "/"  
    
    # Suchen des metadata Elements
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is not None:
        # Suchen des Child-Elements name und dessen Inhalt
        if metadata.find("{*}name") is not None:
            name = metadata.find("{*}name").text
    
    return name
    
def _get_description(input_gpx: gpx) -> str:
    """Sucht die in Metadata definierten Beschreibung der GPX-Datei und gibt diese zurück.

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        str: Name der GPX Datei
    """
    
    # Platzhalter für Beschreibung, falls Element leer ist
    desc = "/" 
    
    # Suchen des metadata Elements
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is not None:
        # Suchen des Child-Elements desc und dessen Inhalt
        if metadata.find("{*}desc") is not None:
            desc = metadata.find("{*}desc").text
    
    return desc
    
def _get_author(input_gpx: gpx) -> AuthorInfo:
    """Sucht die in Metadata definierten Informationen über den Author der GPX-Datei und gibt diese zurück.

    Args:
        input_gpx (gpx): Daten der GPX-Datei

    Returns:
        AuthorInfo: Informationen über den Author
    """
    
    # Platzhalter für Autor Information, falls die entsprechenden Elemente leer sind
    author_info = AuthorInfo("/", "/", "/", "/", "/", "/")
    
    # Suchen des metadata Elements
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is None:     # Falls Element nicht vorhanden Funktion abbrechen
        return author_info
    
    # Suchen des Child-Elements author
    author = metadata.find("{*}author")
    if author is None:      # Falls Element nicht vorhanden Funktion abbrechen
        return author_info
    
    # Suchen des Child-Elemets name und dessen Inhalt
    name = author.find("{*}name")
    if name is not None:
        author_info.name = name.text

    # Suchen des Child-Elemets email und den Inhalt dessen Child-Elements
    email = author.find("{*}email") 
    if email is not None:
        
        author_info.email_id = email.get("id")
        author_info.email_domain = email.get("domain")
    
    # Suchen des Child-Elemets link und den Inhalt dessen Child-Elements
    link = author.find("{*}link")
    if link is not None:
        # Auslesen des Hyperlink
        author_info.href = link.get("href")
        
        # Auslesen von Link Text und Type
        if link.find("{*}text") is not None:
            author_info.link_text = link.find("{*}text").text
        if link.find("{*}type") is not None:
            author_info.link_type = link.find("{*}type").text

    return author_info
    
def edit_name(new_name: str, input_gpx: gpx,) -> None:
    """Ändert den in metadata definierten Namen oder legt diesen an.

    Args:
        new_name (str): Neuer Name / None: keine Änderung
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    # Abbrechen, falls Name nicht geändert werden soll
    if new_name is None:
        return
    
    # Suchen des Elements metadata bzw. erstellen, falls es nicht existiert
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is None:
        input_gpx.append(lxml.etree.Element("metadata"))
        metadata = input_gpx.etree.find("{*}metadata")
        
    # Suchen des Child-Elements name bzw. erstellen, falls es nicht existiert
    name = metadata.find("{*}name")
    if name is None:
        metadata.append(lxml.etree.Element("name"))
        name = metadata.find("{*}name")
    
    # Ändern des Namens
    name.text = new_name
        
def edit_description(new_desc: str, input_gpx: gpx) -> None:
    """Ändert die in metadata definierte Beschreibung oder legt diesen an.

    Args:
        new_desc (str): Neue Beschreibung / None: keine Änderung
        input_gpx (gpx): Daten der GPX-Datei
        
    Returns:
        gpx: Bearbeitete GPX-Daten
    """    
    
    # Abbrechen, falls Beschreibung nicht geändert werden soll
    if new_desc is None:
        return
    
    # Suchen des Elements metadata bzw. erstellen, falls es nicht existiert
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is None:
        input_gpx.append(lxml.etree.Element("metadata"))
        metadata = input_gpx.etree.find("{*}metadata")
        
    # Suchen des Child-Elements desc bzw. erstellen, falls es nicht existiert
    desc = metadata.find("{*}desc")
    if desc is None:
        metadata.append(lxml.etree.Element("desc"))
        desc = metadata.find("{*}desc")
    
    # Ändern des Namens
    desc.text = new_desc
    
def edit_author(new_name: str, new_email: str, new_href: str, new_link_text: str, new_link_type: str, input_gpx: gpx) -> None:
    """_summary_

    Args:
        new_name (str): _description_
        new_email (str): _description_
        new_href (str): _description_
        new_link_text (str): _description_
        new_link_type (str): _description_
        input_gpx (gpx): _description_
    """
    
    # Abbrechen, falls Author-Informationen nicht geändert werden sollen
    if (new_name or new_email or new_href or new_link_text or new_link_type) is None:
        return
    
    # Suchen des Elements metadata bzw. erstellen, falls es nicht existiert
    metadata = input_gpx.etree.find("{*}metadata")
    if metadata is None:
        input_gpx.append(lxml.etree.Element("metadata"))
        metadata = input_gpx.etree.find("{*}metadata")
    
    # Suchen des Child-Elements author bzw. erstellen, falls es nicht existiert
    author = metadata.find("{*}author")
    if author is None:
        metadata.append(lxml.etree.Element("author"))
        author = metadata.find("{*}author")
    
    # Bearbeiten des Namens
    if new_name is not None:
        
        # Suchen des Child-Elements name bzw. erstellen, falls es nicht existiert und schreiben des neuen Werts
        name = author.find("{*}name")
        if name is None:
            author.append(lxml.etree.Element("name"))
            name = author.find("{*}name")
        name.text = new_name
    
    # Bearbeiten der Email
    if new_email is not None:
        # Überprüfen auf gültige Email und Aufteilen in id und domain
        if re.fullmatch(r"^[A-Za-z0-9\.!#\$%&'\*\+-/=\?\^_`\{\|\}~]+@[A-Za-z0-9\.!#\$%&'\*\+-/=\?\^_`\{\|\}~]+\.[a-zA-Z][a-zA-Z]+$", new_email):
            new_id = new_email.split("@")[0]
            new_domain = new_email.split("@")[1]
        else:
            print_error("Error 500: Email im falschen Format angegeben!")
            return

        # Suchen des Child-Elements email bzw. erstellen, falls es nicht existiert und schreiben des neuen Werts
        email = author.find("{*}email")
        if email is None:
            author.append(lxml.etree.Element("email"))
            email = author.find("{*}email")
            
        email.set("id", new_id)
        email.set("domain", new_domain)
        
    # Bearbeiten des Links
    if new_href is not None:
        
        # Suchen des Child-Elements email bzw. erstellen, falls es nicht existiert und schreiben des neuen Werts
        link = author.find("{*}link")
        if link is None:
            author.append(lxml.etree.Element("link"))
            link = author.find("{*}link")
        
        link.set("href", new_href)
        
        # Bearbeiten von Text
        if new_link_text is not None:
            
            # Suchen des Child-Elements email bzw. erstellen, falls es nicht existiert und schreiben des neuen Werts
            text = link.find("{*}text")
            if text is None:
                link.append(lxml.etree.Element("text"))
                text = link.find("{*}text")
            text.text = new_link_text
        
        # Bearbeiten von Type
        if new_link_type is not None:
        
            # Suchen des Child-Elements email bzw. erstellen, falls es nicht existiert und schreiben des neuen Werts
            type = link.find("{*}type")
            if type is None:
                link.append(lxml.etree.Element("type"))
                type = link.find("{*}type")
            type.text = new_link_type
        
    elif new_href is None and (new_link_text or new_link_type) is not None:
        print_error("Error 501: Um Link-Text order Link-Type zu setzen, darf Link nicht leer sein.")
        
def print_name(input_gpx: gpx) -> None:
    """Formatierte Ausgabe des Namens

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    # Abfrage und Ausgabe des Namens
    name = _get_name(input_gpx)
    print_color(f"Name: {name}")

def print_description(input_gpx: gpx) -> None:
    """Formatierte Ausgabe der Beschreibung

    Args:
        input_gpx (gpx): Daten der GPX-Datei
    """
    
    # Abfrage und Ausgabe der Beschreibung
    description = _get_description(input_gpx)
    print_color(f"Beschreibung: {description}")
    
    return

def print_author(input_gpx: gpx, long: bool = False) -> None:
    """Formatierte Ausgabe der Author-Informationen

    Args:
        input_gpx (gpx): Daten der GPX-Datei
        long (bool, optional): Erweiterte Ausgabe. Defaults to False.
    """   
    
    # Abfragen aller Author-Informationen
    author = _get_author(input_gpx)
    
    # Erweiterte Ausgabe der Author-Informationen
    if long is True:
        print_color("Autor:")
        print_color(f"  Name: {author.name}")
        if (author.email_id and author.email_domain) != "/":
            print_color(f"  Email: {author.email_id}@{author.email_domain}")
        else:
            print_color("  Email: /")
        print_color(f"  Link: {author.href}")
        print_color(f"    Text: {author.link_text}")
        print_color(f"    Typ des Inhalts: {author.link_type}")
        
    # Kurze Ausgabe der Author-Informationen
    else:
        print_color(f"Autor: {author.name}")
        
    return