import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from ...config import EXTENSIONS_DISPONIBLES, THEMES_DISPONIBLES
from ...historique import charger_historique, effacer_historique
from ...i18n import LANGUES_DISPONIBLES
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen

NOM_PAR_CODE = dict(LANGUES_DISPONIBLES)
CODE_PAR_NOM = {nom: code for code, nom in LANGUES_DISPONIBLES}


class ParametresScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        conteneur = ctk.CTkFrame(self, fg_color="transparent")
        conteneur.pack(fill='both', expand=True, padx=32, pady=28)

        self.label_titre = ctk.CTkLabel(conteneur, text=self.t("parametres.titre"), font=font_titre(20))
        self.label_titre.pack(anchor='w', pady=(0, 10))

        self.label_sous_titre = ctk.CTkLabel(
            conteneur, text=self.t("parametres.sous_titre"), font=font_sous_titre(12), text_color="gray",
        )
        self.label_sous_titre.pack(anchor='w', pady=(0, 6))

        # Langue
        self.label_section_langue = ctk.CTkLabel(
            conteneur, text=self.t("parametres.section_langue"), font=font_normal(14, "bold"))
        self.label_section_langue.pack(anchor='w')
        self.label_langue = ctk.CTkLabel(
            conteneur, text=self.t("parametres.langue_label"), font=font_sous_titre(12), text_color="gray",
        )
        self.label_langue.pack(anchor='w', pady=(0, 6))
        self.langue_var = tk.StringVar(value=NOM_PAR_CODE.get(app.config.langue, NOM_PAR_CODE[app.i18n.langue]))
        self.selecteur_langue = ctk.CTkSegmentedButton(
            conteneur, values=[nom for _, nom in LANGUES_DISPONIBLES],
            variable=self.langue_var, command=self._changer_langue,
        )
        self.selecteur_langue.pack(anchor='w', pady=(0, 24))

        # Thème
        self.label_section_apparence = ctk.CTkLabel(
            conteneur, text=self.t("parametres.section_apparence"), font=font_normal(14, "bold"))
        self.label_section_apparence.pack(anchor='w')
        self.label_theme = ctk.CTkLabel(
            conteneur, text=self.t("parametres.theme_label"), font=font_sous_titre(12), text_color="gray",
        )
        self.label_theme.pack(anchor='w', pady=(0, 6))
        self.theme_var = tk.StringVar(value=app.config.theme)
        ctk.CTkSegmentedButton(
            conteneur, values=THEMES_DISPONIBLES, variable=self.theme_var, command=self._changer_theme,
        ).pack(anchor='w', pady=(0, 24))

        # Extensions par défaut
        self.label_section_recherche = ctk.CTkLabel(
            conteneur, text=self.t("parametres.section_recherche"), font=font_normal(14, "bold"))
        self.label_section_recherche.pack(anchor='w')
        self.label_extensions = ctk.CTkLabel(
            conteneur, text=self.t("parametres.extensions_label"), font=font_sous_titre(12), text_color="gray",
        )
        self.label_extensions.pack(anchor='w', pady=(0, 6))
        extensions_frame = ctk.CTkFrame(conteneur, fg_color="transparent")
        extensions_frame.pack(anchor='w', pady=(0, 24))
        self.extension_vars = {}
        for ext in EXTENSIONS_DISPONIBLES:
            var = tk.BooleanVar(value=ext in app.config.extensions_par_defaut)
            var.trace_add("write", lambda *_: self._changer_extensions())
            ctk.CTkCheckBox(extensions_frame, text=ext, variable=var).pack(side='left', padx=(0, 14))
            self.extension_vars[ext] = var

        # Historique
        self.label_section_historique = ctk.CTkLabel(
            conteneur, text=self.t("parametres.section_historique"), font=font_normal(14, "bold"))
        self.label_section_historique.pack(anchor='w')
        self.label_historique = ctk.CTkLabel(conteneur, text="", font=font_sous_titre(12), text_color="gray")
        self.label_historique.pack(anchor='w', pady=(0, 8))
        self.bouton_effacer_historique = ctk.CTkButton(
            conteneur, text=self.t("parametres.effacer_historique"), fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=self._effacer_historique,
        )
        self.bouton_effacer_historique.pack(anchor='w')

    def retraduire(self):
        self.label_titre.configure(text=self.t("parametres.titre"))
        self.label_sous_titre.configure(text=self.t("parametres.sous_titre"))
        self.label_section_langue.configure(text=self.t("parametres.section_langue"))
        self.label_langue.configure(text=self.t("parametres.langue_label"))
        self.selecteur_langue.configure(values=[nom for _, nom in LANGUES_DISPONIBLES])
        self.langue_var.set(NOM_PAR_CODE[self.app.i18n.langue])
        self.label_section_apparence.configure(text=self.t("parametres.section_apparence"))
        self.label_theme.configure(text=self.t("parametres.theme_label"))
        self.label_section_recherche.configure(text=self.t("parametres.section_recherche"))
        self.label_extensions.configure(text=self.t("parametres.extensions_label"))
        self.label_section_historique.configure(text=self.t("parametres.section_historique"))
        self.bouton_effacer_historique.configure(text=self.t("parametres.effacer_historique"))
        self._maj_label_historique()

    def on_show(self, **kwargs):
        self.theme_var.set(self.app.config.theme)
        self.langue_var.set(NOM_PAR_CODE[self.app.i18n.langue])
        self._maj_label_historique()

    def _maj_label_historique(self):
        n = len(charger_historique())
        self.label_historique.configure(
            text=self.t("parametres.historique_compte", n=n) if n else self.t("parametres.historique_vide"))

    def _changer_theme(self, valeur):
        ctk.set_appearance_mode(valeur)
        self.app.config.definir_theme(valeur)

    def _changer_extensions(self):
        extensions = [ext for ext, var in self.extension_vars.items() if var.get()]
        self.app.config.definir_extensions_par_defaut(extensions)

    def _changer_langue(self, nom):
        code = CODE_PAR_NOM.get(nom)
        if code:
            self.app.changer_langue(code)

    def _effacer_historique(self):
        if messagebox.askyesno(self.t("parametres.confirmer_titre"), self.t("parametres.confirmer_message")):
            effacer_historique()
            self._maj_label_historique()
