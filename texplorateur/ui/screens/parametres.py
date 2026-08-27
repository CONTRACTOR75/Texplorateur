import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ...config import EXTENSIONS_DISPONIBLES, THEMES_DISPONIBLES
from ...historique import charger_historique, effacer_historique
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class ParametresScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        conteneur = ctk.CTkFrame(self, fg_color="transparent")
        conteneur.pack(fill='both', expand=True, padx=32, pady=28)

        ctk.CTkLabel(conteneur, text="Paramètres", font=font_titre(20)).pack(anchor='w', pady=(0, 10))

        ctk.CTkLabel(
                    conteneur, text="Paramètrez et gerez ici vos options par défaut", font=font_sous_titre(12), text_color="gray",
                ).pack(anchor='w', pady=(0, 6))

        # Thème
        ctk.CTkLabel(conteneur, text="Apparence", font=font_normal(14, "bold")).pack(anchor='w')
        ctk.CTkLabel(
            conteneur, text="Thème de l'interface", font=font_sous_titre(12), text_color="gray",
        ).pack(anchor='w', pady=(0, 6))
        self.theme_var = tk.StringVar(value=app.config.theme)
        ctk.CTkSegmentedButton(
            conteneur, values=THEMES_DISPONIBLES, variable=self.theme_var, command=self._changer_theme,
        ).pack(anchor='w', pady=(0, 24))

        # Extensions par défaut
        ctk.CTkLabel(conteneur, text="Recherche", font=font_normal(14, "bold")).pack(anchor='w')
        ctk.CTkLabel(
            conteneur, text="Types de fichiers pré-cochés à l'ouverture du formulaire",
            font=font_sous_titre(12), text_color="gray",
        ).pack(anchor='w', pady=(0, 6))
        extensions_frame = ctk.CTkFrame(conteneur, fg_color="transparent")
        extensions_frame.pack(anchor='w', pady=(0, 24))
        self.extension_vars = {}
        for ext in EXTENSIONS_DISPONIBLES:
            var = tk.BooleanVar(value=ext in app.config.extensions_par_defaut)
            var.trace_add("write", lambda *_: self._changer_extensions())
            ctk.CTkCheckBox(extensions_frame, text=ext, variable=var).pack(side='left', padx=(0, 14))
            self.extension_vars[ext] = var

        # Historique
        ctk.CTkLabel(conteneur, text="Historique", font=font_normal(14, "bold")).pack(anchor='w')
        self.label_historique = ctk.CTkLabel(conteneur, text="", font=font_sous_titre(12), text_color="gray")
        self.label_historique.pack(anchor='w', pady=(0, 8))
        ctk.CTkButton(
            conteneur, text="Effacer l'historique", fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=self._effacer_historique,
        ).pack(anchor='w')

    def on_show(self, **kwargs):
        self.theme_var.set(self.app.config.theme)
        self._maj_label_historique()

    def _maj_label_historique(self):
        n = len(charger_historique())
        self.label_historique.configure(
            text=f"{n} recherche(s) enregistrée(s)" if n else "Aucune recherche enregistrée")

    def _changer_theme(self, valeur):
        ctk.set_appearance_mode(valeur)
        self.app.config.definir_theme(valeur)

    def _changer_extensions(self):
        extensions = [ext for ext, var in self.extension_vars.items() if var.get()]
        self.app.config.definir_extensions_par_defaut(extensions)

    def _effacer_historique(self):
        if messagebox.askyesno("Effacer l'historique", "Supprimer définitivement tout l'historique des recherches ?"):
            effacer_historique()
            self._maj_label_historique()
