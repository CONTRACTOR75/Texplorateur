import customtkinter as ctk

from ...historique import charger_historique, libelle_historique
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class AccueilScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        centre = ctk.CTkFrame(self, fg_color="transparent")
        centre.place(relx=0.5, rely=0.42, anchor="center")

        ctk.CTkLabel(centre, text="🗂️", font=ctk.CTkFont(size=48)).pack()
        ctk.CTkLabel(centre, text="Texplorateur", font=font_titre(28)).pack(pady=(8, 2))
        ctk.CTkLabel(
            centre, text="Retrouvez une phrase dans vos fichiers, en un instant.",
            font=font_sous_titre(13), text_color="gray",
        ).pack(pady=(0, 24))

        ctk.CTkButton(
            centre, text="+ Nouvelle recherche", height=42, width=220,
            font=font_normal(14, "bold"),
            command=lambda: self.app.navigate("formulaire"),
        ).pack()

        self.label_raccourci = ctk.CTkLabel(
            centre, text="", font=font_sous_titre(12), text_color="gray", cursor="hand2",
        )
        self.label_raccourci.pack(pady=(18, 0))

        self.label_stats = ctk.CTkLabel(centre, text="", font=font_sous_titre(11), text_color="gray")
        self.label_stats.pack(pady=(4, 0))

    def on_show(self, **kwargs):
        historique = charger_historique()

        if historique:
            derniere = historique[0]
            self.label_raccourci.configure(text=f"↻ Relancer : {libelle_historique(derniere)}")
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
            text=f"{n} recherche(s) dans l'historique" if n else "Aucune recherche pour l'instant")
