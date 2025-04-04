# utils.py
import re
from datetime import datetime

def convertir_date(pdf_timestamp):
    """Convertit un timestamp PDF en date ISO."""
    date_obj = datetime.strptime(pdf_timestamp[2:10], "%Y%m%d").date()
    return date_obj.isoformat()

def convert_pdf_timestamp_to_iso_date(pdf_timestamp):
    """Convertit un timestamp PDF en date ISO (extraction de la partie YYYYMMDD)."""
    pdf_timestamp = pdf_timestamp[2:]
    timestamp_str = pdf_timestamp[:8]
    date_obj = datetime.strptime(timestamp_str, "%Y%m%d").date()
    return date_obj.isoformat()

def normalize_name(name):
    """Nettoie un nom pour l'utiliser dans un fichier (remplacement des caractères spéciaux)."""
    name = name.lower().strip()
    name = re.sub(r"\W+", "_", name)
    return name.strip("_")

def extract_title_and_author(title_text):
    """Extrait le titre et l'auteur d'un texte de titre en markdown."""
    author = None
    match = re.search(r"^(.+?)[\s\-\(](.*?)[\)]?$", title_text)
    
    if match and len(match.groups()) == 2:
        title = match.group(1).strip()
        possible_author = match.group(2).strip()

        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)?$", possible_author):
            author = possible_author
        else:
            title = title_text.strip()
    else:
        title = title_text.strip()
    
    return title, author if author else "inconnu"
