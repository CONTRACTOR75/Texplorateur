from tkinter import messagebox

import customtkinter as ctk

from ...historique import charger_historique, supprimer_historique
from ..theme import ACCENT_ERREUR, ACCENT_GRIS, font_normal, font_sous_titre, font_titre
from .base import Screen


class HistoriqueScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.label_titre = ctk.CTkLabel(self, text=self.t("historique.titre"), font=font_titre(20))
        self.label_titre.pack(anchor='w', padx=24, pady=(24, 4))
        self.corps = ctk.CTkFrame(self, fg_color="transparent")
        self.corps.pack(fill='both', expand=True, padx=16, pady=(4, 16))
        self.corps.grid_columnconfigure(0, weight=1)
        self.corps.grid_rowconfigure(0, weight=1)

        self.label_vide = ctk.CTkLabel(
            self.corps, text=self.t("historique.vide"), font=font_sous_titre(12), text_color=ACCENT_GRIS)
        self.label_vide.grid(row=0, column=0, sticky='nw', padx=8, pady=8)

        self.liste = ctk.CTkScrollableFrame(self.corps, fg_color="transparent")
        self.liste.grid(row=0, column=0, sticky='nsew')

    def retraduire(self):
        self.label_titre.configure(text=self.t("historique.titre"))
        self.label_vide.configure(text=self.t("historique.vide"))

    def on_show(self, **kwargs):
        for widget in self.liste.winfo_children():
            widget.destroy()

        historique = charger_historique()
        if not historique:
            self.liste.grid_remove()
            self.label_vide.grid()
            return
        self.label_vide.grid_remove()
        self.liste.grid()

        for entree in historique:
            self._afficher_entree(entree)

    def _afficher_entree(self, entree):
        carte = ctk.CTkFrame(self.liste)
        carte.pack(fill='x', padx=4, pady=4)

        contenu = ctk.CTkFrame(carte, fg_color="transparent")
        contenu.pack(fill='x', padx=12, pady=10)

        ctk.CTkLabel(contenu, text=f'"{entree["phrase"]}"', font=font_normal(13, "bold"), anchor='w').pack(
            fill='x')
        ctk.CTkLabel(
            contenu, text=f'{", ".join(entree["extensions"])} — {entree["dossier"]}',
            font=font_sous_titre(11), text_color=ACCENT_GRIS, anchor='w', wraplength=600,
        ).pack(fill='x', pady=(2, 8))

        boutons = ctk.CTkFrame(contenu, fg_color="transparent")
        boutons.pack(anchor='e')

        # Les entrées enregistrées avant l'ajout de cette fonctionnalité
        # n'ont pas de résultats sauvegardés : le bouton reste désactivé
        # plutôt que de planter ou d'afficher un écran vide trompeur.
        resultats_disponibles = "resultats" in entree
        ctk.CTkButton(
            boutons, text=self.t("commun.resultats"), width=110,
            state="normal" if resultats_disponibles else "disabled",
            command=lambda e=entree: self.app.afficher_resultats_historique(e),
        ).pack(side='left', padx=(0, 8))

        ctk.CTkButton(
            boutons, text=self.t("commun.relancer"), width=110, fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"),
            command=lambda e=entree: self.app.lancer_recherche(e["phrase"], e["extensions"], e["dossier"]),
        ).pack(side='left')

        ctk.CTkButton(
            boutons, text=self.t("commun.supprimer"), width=36, anchor="center", fg_color="transparent", border_width=1,
            text_color=ACCENT_ERREUR,
            hover_color=("#f5d0d0", "#4a2626"),
            # Police par défaut (Segoe UI) sans glyphe emoji correct : le
            # rendu tombe sur un fallback plus large et mal centré, qui
            # pousse même le bouton au-delà du width demandé. Une police
            # emoji explicite règle la taille ET le centrage (vérifié par
            # mesure de pixels : décalage de 9.5px -> 0.5px).
            font=ctk.CTkFont(family="Segoe UI Emoji", size=14),
            command=lambda e=entree: self._supprimer(e),
        ).pack(side="left", padx=(8, 0))

    def _supprimer(self, entree):
        if messagebox.askyesno(
            self.t("historique.confirmer_suppression_titre"),
            self.t("historique.confirmer_suppression_message", phrase=entree["phrase"]),
        ):
            supprimer_historique(entree)
            self.on_show()
