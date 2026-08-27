import os
import subprocess
from tkinter import messagebox


def ouvrir_emplacement(chemin):
    try:
        chemin_normalise = os.path.normpath(chemin)
        if os.name == 'nt':
            subprocess.Popen(f'explorer /select,"{chemin_normalise}"')
        else:
            dossier = os.path.dirname(chemin_normalise)
            subprocess.Popen(['xdg-open', dossier])
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'explorateur: {str(e)}")
