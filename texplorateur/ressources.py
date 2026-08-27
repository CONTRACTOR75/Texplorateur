import os
import sys

ICONE_NOM = "image.ico"


def chemin_ressource(nom_fichier):
    """Résout le chemin d'un fichier de ressource (racine du projet en
    développement, dossier temporaire d'extraction une fois compilé avec
    PyInstaller)."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        # texplorateur/ressources.py -> texplorateur/ -> racine du projet
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nom_fichier)


def chemin_icone():
    return chemin_ressource(ICONE_NOM)
