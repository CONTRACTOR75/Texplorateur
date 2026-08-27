import webbrowser

import customtkinter as ctk

from ..theme import ACCENT_LIEN, ACCENT_LIEN_SURVOL, font_normal, font_sous_titre, font_titre
from .base import Screen

VERSION = "2.0"

# TODO(CONTRACTOR75) : remplacer par l'URL du portfolio.
URL_PORTFOLIO = "https://aledi.netlify.app/"


class AProposScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        centre = ctk.CTkFrame(self, fg_color="transparent")
        centre.place(relx=0.5, rely=0.4, anchor="center")

        # Police emoji explicite requise pour un centrage correct — voir
        # accueil.py pour le détail (sans elle, Tk retombe sur un glyphe de
        # secours mal centré et bien plus large que le libellé du dessous).
        ctk.CTkLabel(centre, text="🗂️", font=ctk.CTkFont(family="Segoe UI Emoji", size=40)).pack()
        # "Texplorateur" est le nom de l'app : pas de traduction.
        ctk.CTkLabel(centre, text="Texplorateur", font=font_titre(22)).pack(pady=(6, 0))
        self.label_version = ctk.CTkLabel(
            centre, text=self.t("a_propos.version", version=VERSION), font=font_sous_titre(12), text_color="gray")
        self.label_version.pack(pady=(0, 16))

        self.label_description = ctk.CTkLabel(
            centre, text=self.t("a_propos.description"), font=font_sous_titre(13), justify="center")
        self.label_description.pack(pady=(0, 16))

        ligne_auteur = ctk.CTkFrame(centre, fg_color="transparent")
        ligne_auteur.pack()
        self.label_auteur_prefixe = ctk.CTkLabel(
            ligne_auteur, text=self.t("a_propos.auteur_prefixe"), font=font_sous_titre(12), text_color="gray")
        self.label_auteur_prefixe.pack(side='left')
        # "CONTRACTOR75" est un nom propre : pas de traduction.
        self.lien_auteur = ctk.CTkLabel(
            ligne_auteur, text=" CONTRACTOR75", font=font_normal(12, "bold"),
            text_color=ACCENT_LIEN, cursor="hand2",
        )
        self.lien_auteur.pack(side='left')
        self.lien_auteur.bind("<Button-1>", self._ouvrir_portfolio)
        self.lien_auteur.bind("<Enter>", lambda e: self.lien_auteur.configure(text_color=ACCENT_LIEN_SURVOL))
        self.lien_auteur.bind("<Leave>", lambda e: self.lien_auteur.configure(text_color=ACCENT_LIEN))

    def retraduire(self):
        self.label_version.configure(text=self.t("a_propos.version", version=VERSION))
        self.label_description.configure(text=self.t("a_propos.description"))
        self.label_auteur_prefixe.configure(text=self.t("a_propos.auteur_prefixe"))

    def _ouvrir_portfolio(self, event=None):
        if URL_PORTFOLIO:
            webbrowser.open(URL_PORTFOLIO)
