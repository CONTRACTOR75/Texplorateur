import customtkinter as ctk

from ...historique import charger_historique
from ..theme import font_normal, font_sous_titre, font_titre
from .base import Screen


class HistoriqueScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        ctk.CTkLabel(self, text="Historique des recherches", font=font_titre(20)).pack(
            anchor='w', padx=24, pady=(24, 4))
        self.label_vide = ctk.CTkLabel(
            self, text="Aucune recherche pour l'instant.", font=font_sous_titre(12), text_color="gray")

        self.liste = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.liste.pack(fill='both', expand=True, padx=16, pady=(4, 16))

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

        ctk.CTkButton(
            contenu, text="↻ Relancer", width=110,
            command=lambda e=entree: self.app.lancer_recherche(e["phrase"], e["extensions"], e["dossier"]),
        ).pack(anchor='e')
