import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ...config import EXTENSIONS_DISPONIBLES
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class FormulaireScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.dossier_selectionne = None

        ctk.CTkButton(
            self, text="← Accueil", fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"), width=100, anchor='w',
            command=lambda: self.app.navigate("accueil"),
        ).place(x=16, y=16)

        carte = ctk.CTkFrame(self, corner_radius=14)
        carte.place(relx=0.5, rely=0.46, anchor="center")
        contenu = ctk.CTkFrame(carte, fg_color="transparent")
        contenu.pack(padx=40, pady=32)

        ctk.CTkLabel(contenu, text="Nouvelle recherche", font=font_titre(20)).pack(anchor='w', pady=(0, 18))

        ctk.CTkLabel(contenu, text="Phrase à rechercher :", font=font_sous_titre(12)).pack(anchor='w')
        self.champ_phrase = ctk.CTkEntry(contenu, placeholder_text="Ex : rapport annuel 2025", width=380)
        self.champ_phrase.pack(fill='x', pady=(2, 16))

        ctk.CTkLabel(contenu, text="Dossier de recherche :", font=font_sous_titre(12)).pack(anchor='w')
        dossier_frame = ctk.CTkFrame(contenu, fg_color="transparent")
        dossier_frame.pack(fill='x', pady=(2, 16))
        self.label_dossier = ctk.CTkLabel(dossier_frame, text="Aucun dossier sélectionné", text_color="gray", anchor='w')
        self.label_dossier.pack(side='left', fill='x', expand=True)
        ctk.CTkButton(dossier_frame, text="Parcourir…", width=100, command=self._choisir_dossier).pack(side='right')

        ctk.CTkLabel(contenu, text="Types de fichiers :", font=font_sous_titre(12)).pack(anchor='w')
        extensions_frame = ctk.CTkFrame(contenu, fg_color="transparent")
        extensions_frame.pack(fill='x', pady=(2, 24))
        self.extension_vars = {}
        for ext in EXTENSIONS_DISPONIBLES:
            var = tk.BooleanVar(value=False)
            ctk.CTkCheckBox(extensions_frame, text=ext, variable=var).pack(side='left', padx=(0, 14))
            self.extension_vars[ext] = var

        ctk.CTkButton(
            contenu, text="Rechercher", height=38, font=font_normal(14, "bold"),
            command=self._valider,
        ).pack(fill='x')

    def on_show(self, **kwargs):
        for ext, var in self.extension_vars.items():
            var.set(ext in self.app.config.extensions_par_defaut)
        if self.dossier_selectionne:
            self.label_dossier.configure(text=self.dossier_selectionne, text_color=("black", "white"))

    def _choisir_dossier(self):
        dossier = filedialog.askdirectory(title="Choisir le dossier de départ")
        if dossier:
            self.dossier_selectionne = dossier
            self.label_dossier.configure(text=dossier, text_color=("black", "white"))

    def _valider(self):
        phrase = self.champ_phrase.get().strip()
        extensions = [ext for ext, var in self.extension_vars.items() if var.get()]

        if not phrase or not extensions or not self.dossier_selectionne:
            messagebox.showwarning(
                "Champs requis",
                "Veuillez saisir une phrase, sélectionner un dossier et au moins un type de fichier.")
            return

        self.app.lancer_recherche(phrase, extensions, self.dossier_selectionne)
