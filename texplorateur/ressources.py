import os
import sys

import customtkinter as ctk
from PIL import Image

ICONE_NOM = "image.ico"

_cache_images = {}


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


def image_icone(taille):
    """CTkImage du logo (image.ico), mise en cache par taille. `taille` est
    un entier (pixels, carré) — l'ico embarque plusieurs résolutions
    (16 à 256px), donc le sous-échantillonnage reste net."""
    cle = int(taille)
    if cle not in _cache_images:
        pillow_img = Image.open(chemin_icone())
        pillow_img = pillow_img.resize((cle, cle), Image.LANCZOS)
        _cache_images[cle] = ctk.CTkImage(light_image=pillow_img, dark_image=pillow_img, size=(cle, cle))
    return _cache_images[cle]
