import customtkinter as ctk

from ...historique import charger_historique, libelle_historique
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class AccueilScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        centre = ctk.CTkFrame(self, fg_color="transparent")
        centre.place(relx=0.5, rely=0.42, anchor="center")

        # Sans famille de police explicite, Segoe UI (police par défaut) n'a
        # pas de glyphe emoji correct : Tk retombe sur un fallback bien plus
        # large et mal centré (vérifié par mesure de pixels : décalage de
        # 33.5px -> 0.5px une fois la police emoji précisée).
        ctk.CTkLabel(centre, text="🗂️", font=ctk.CTkFont(family="Segoe UI Emoji", size=48)).pack()
        # "Texplorateur" est le nom de l'app : pas de traduction.
        ctk.CTkLabel(centre, text="Texplorateur", font=font_titre(28)).pack(pady=(8, 2))
        self.label_sous_titre = ctk.CTkLabel(
            centre, text=self.t("accueil.sous_titre"), font=font_sous_titre(13), text_color="gray",
        )
        self.label_sous_titre.pack(pady=(0, 24))

        self.bouton_nouvelle_recherche = ctk.CTkButton(
            centre, text=self.t("commun.nouvelle_recherche"), height=42, width=220,
            font=font_normal(14, "bold"),
            command=lambda: self.app.navigate("formulaire"),
        )
        self.bouton_nouvelle_recherche.pack()

        self.label_raccourci = ctk.CTkLabel(
            centre, text="", font=font_sous_titre(12), text_color="gray", cursor="hand2",
        )
        self.label_raccourci.pack(pady=(18, 0))

        self.label_stats = ctk.CTkLabel(centre, text="", font=font_sous_titre(11), text_color="gray")
        self.label_stats.pack(pady=(4, 0))

    def retraduire(self):
        self.label_sous_titre.configure(text=self.t("accueil.sous_titre"))
        self.bouton_nouvelle_recherche.configure(text=self.t("commun.nouvelle_recherche"))

    def on_show(self, **kwargs):
        historique = charger_historique()

        if historique:
            derniere = historique[0]
            self.label_raccourci.configure(
                text=self.t("accueil.raccourci_relancer", libelle=libelle_historique(derniere)))
            self.label_raccourci.bind(
                "<Button-1>",
                lambda e, entree=derniere: self.app.lancer_recherche(
                    entree["phrase"], entree["extensions"], entree["dossier"]),
            )
        else:
            self.label_raccourci.configure(text="")
            self.label_raccourci.unbind("<Button-1>")

        n = len(historique)
        self.label_stats.configure(
            text=self.t("accueil.stats_recherches", n=n) if n else self.t("accueil.stats_vide"))
