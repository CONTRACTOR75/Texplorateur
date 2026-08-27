import customtkinter as ctk

from ...historique import charger_historique
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class HistoriqueScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.label_titre = ctk.CTkLabel(self, text=self.t("historique.titre"), font=font_titre(20))
        self.label_titre.pack(anchor='w', padx=24, pady=(24, 4))
        self.label_vide = ctk.CTkLabel(
            self, text=self.t("historique.vide"), font=font_sous_titre(12), text_color="gray")

        self.liste = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.liste.pack(fill='both', expand=True, padx=16, pady=(4, 16))

    def retraduire(self):
        self.label_titre.configure(text=self.t("historique.titre"))
        self.label_vide.configure(text=self.t("historique.vide"))

    def on_show(self, **kwargs):
        for widget in self.liste.winfo_children():
            widget.destroy()

        historique = charger_historique()
        if not historique:
            self.label_vide.pack(anchor='w', padx=24, pady=(8, 0))
            return
        self.label_vide.pack_forget()

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
            font=font_sous_titre(11), text_color="gray", anchor='w', wraplength=600,
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
