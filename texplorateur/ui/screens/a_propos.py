import webbrowser

import customtkinter as ctk

from ..theme import ACCENT_LIEN, ACCENT_LIEN_SURVOL, font_normal, font_sous_titre, font_titre
from .base import Screen

VERSION = "2.0"

# TODO(CONTRACTOR75) : remplacer par l'URL du portfolio.
URL_PORTFOLIO = "https://aledi.netlify.app/"

# TODO(CONTRACTOR75) : coller le lien du Google Form ici. Tant qu'il est
# vide, le bloc "signaler un bug / avis" ne s'affiche pas du tout.
URL_FEEDBACK = ""


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
        self.lien_auteur = self._creer_lien(
            ligne_auteur, " CONTRACTOR75", URL_PORTFOLIO, cote='left', font=font_normal(12, "bold"))

        # Bloc feedback : entièrement absent tant qu'aucun lien n'est fourni,
        # plutôt qu'affiché avec un lien mort ou désactivé.
        self.label_feedback_message = None
        self.lien_feedback = None
        if URL_FEEDBACK:
            self.label_feedback_message = ctk.CTkLabel(
                centre, text=self.t("a_propos.feedback_message"), font=font_sous_titre(11),
                text_color="gray", justify="center", wraplength=300,
            )
            self.label_feedback_message.pack(pady=(20, 2))
            self.lien_feedback = self._creer_lien(
                centre, self.t("a_propos.feedback_lien"), URL_FEEDBACK, cote=None, font=font_normal(12, "bold"))

    def _creer_lien(self, parent, texte, url, cote, font):
        lien = ctk.CTkLabel(parent, text=texte, font=font, text_color=ACCENT_LIEN, cursor="hand2")
        if cote:
            lien.pack(side=cote)
        else:
            lien.pack()
        lien.bind("<Button-1>", lambda e, u=url: webbrowser.open(u) if u else None)
        lien.bind("<Enter>", lambda e: lien.configure(text_color=ACCENT_LIEN_SURVOL))
        lien.bind("<Leave>", lambda e: lien.configure(text_color=ACCENT_LIEN))
        return lien

    def retraduire(self):
        self.label_version.configure(text=self.t("a_propos.version", version=VERSION))
        self.label_description.configure(text=self.t("a_propos.description"))
        self.label_auteur_prefixe.configure(text=self.t("a_propos.auteur_prefixe"))
        if self.label_feedback_message is not None:
            self.label_feedback_message.configure(text=self.t("a_propos.feedback_message"))
        if self.lien_feedback is not None:
            self.lien_feedback.configure(text=self.t("a_propos.feedback_lien"))
