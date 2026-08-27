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

        self.bouton_retour = ctk.CTkButton(
            self, text=self.t("commun.retour_accueil"), fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"), width=100, anchor='w',
            command=lambda: self.app.navigate("accueil"),
        )
        self.bouton_retour.place(x=16, y=16)

        carte = ctk.CTkFrame(self, corner_radius=14)
        carte.place(relx=0.5, rely=0.46, anchor="center")
        contenu = ctk.CTkFrame(carte, fg_color="transparent")
        contenu.pack(padx=40, pady=32)

        self.label_titre = ctk.CTkLabel(contenu, text=self.t("formulaire.titre"), font=font_titre(20))
        self.label_titre.pack(anchor='w', pady=(0, 18))

        self.label_phrase = ctk.CTkLabel(contenu, text=self.t("formulaire.label_phrase"), font=font_sous_titre(12))
        self.label_phrase.pack(anchor='w')
        self.champ_phrase = ctk.CTkEntry(
            contenu, placeholder_text=self.t("formulaire.placeholder_phrase"), width=380)
        self.champ_phrase.pack(fill='x', pady=(2, 16))

        self.label_dossier_titre = ctk.CTkLabel(
            contenu, text=self.t("formulaire.label_dossier"), font=font_sous_titre(12))
        self.label_dossier_titre.pack(anchor='w')
        dossier_frame = ctk.CTkFrame(contenu, fg_color="transparent")
        dossier_frame.pack(fill='x', pady=(2, 16))
        self.label_dossier = ctk.CTkLabel(
            dossier_frame, text=self.t("formulaire.dossier_non_selectionne"), text_color="gray", anchor='w')
        self.label_dossier.pack(side='left', fill='x', expand=True)
        self.bouton_parcourir = ctk.CTkButton(
            dossier_frame, text=self.t("commun.parcourir"), width=100, command=self._choisir_dossier)
        self.bouton_parcourir.pack(side='right')

        self.label_extensions = ctk.CTkLabel(
            contenu, text=self.t("formulaire.label_extensions"), font=font_sous_titre(12))
        self.label_extensions.pack(anchor='w')
        extensions_frame = ctk.CTkFrame(contenu, fg_color="transparent")
        extensions_frame.pack(fill='x', pady=(2, 24))
        self.extension_vars = {}
        for ext in EXTENSIONS_DISPONIBLES:
            var = tk.BooleanVar(value=False)
            ctk.CTkCheckBox(extensions_frame, text=ext, variable=var).pack(side='left', padx=(0, 14))
            self.extension_vars[ext] = var

        self.bouton_rechercher = ctk.CTkButton(
            contenu, text=self.t("commun.rechercher"), height=38, font=font_normal(14, "bold"),
            command=self._valider,
        )
        self.bouton_rechercher.pack(fill='x')

    def retraduire(self):
        self.bouton_retour.configure(text=self.t("commun.retour_accueil"))
        self.label_titre.configure(text=self.t("formulaire.titre"))
        self.label_phrase.configure(text=self.t("formulaire.label_phrase"))
        self.champ_phrase.configure(placeholder_text=self.t("formulaire.placeholder_phrase"))
        self.label_dossier_titre.configure(text=self.t("formulaire.label_dossier"))
        # Ne pas écraser le chemin déjà affiché si un dossier est sélectionné.
        if not self.dossier_selectionne:
            self.label_dossier.configure(text=self.t("formulaire.dossier_non_selectionne"))
        self.bouton_parcourir.configure(text=self.t("commun.parcourir"))
        self.label_extensions.configure(text=self.t("formulaire.label_extensions"))
        self.bouton_rechercher.configure(text=self.t("commun.rechercher"))

    def on_show(self, **kwargs):
        for ext, var in self.extension_vars.items():
            var.set(ext in self.app.config.extensions_par_defaut)
        if self.dossier_selectionne:
            self.label_dossier.configure(text=self.dossier_selectionne, text_color=("black", "white"))

    def _choisir_dossier(self):
        dossier = filedialog.askdirectory(title=self.t("formulaire.label_dossier"))
        if dossier:
            self.dossier_selectionne = dossier
            self.label_dossier.configure(text=dossier, text_color=("black", "white"))

    def _valider(self):
        phrase = self.champ_phrase.get().strip()
        extensions = [ext for ext, var in self.extension_vars.items() if var.get()]

        if not phrase or not extensions or not self.dossier_selectionne:
            messagebox.showwarning(
                self.t("formulaire.erreur_champs_titre"), self.t("formulaire.erreur_champs_message"))
            return

        self.app.lancer_recherche(phrase, extensions, self.dossier_selectionne)
