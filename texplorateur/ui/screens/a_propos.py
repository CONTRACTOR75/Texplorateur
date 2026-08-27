import customtkinter as ctk

from ..theme import font_sous_titre, font_titre
from .base import Screen

VERSION = "2.0"


class AProposScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        centre = ctk.CTkFrame(self, fg_color="transparent")
        centre.place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(centre, text="🗂️", font=ctk.CTkFont(size=40)).pack()
        # "Texplorateur" est le nom de l'app : pas de traduction.
        ctk.CTkLabel(centre, text="Texplorateur", font=font_titre(22)).pack(pady=(6, 0))
        self.label_version = ctk.CTkLabel(
            centre, text=self.t("a_propos.version", version=VERSION), font=font_sous_titre(12), text_color="gray")
        self.label_version.pack(pady=(0, 16))

        self.label_description = ctk.CTkLabel(
            centre, text=self.t("a_propos.description"), font=font_sous_titre(13), justify="center")
        self.label_description.pack(pady=(0, 16))

        self.label_auteur = ctk.CTkLabel(
            centre, text=self.t("a_propos.auteur"), font=font_sous_titre(12), text_color="gray")
        self.label_auteur.pack()

    def retraduire(self):
        self.label_version.configure(text=self.t("a_propos.version", version=VERSION))
        self.label_description.configure(text=self.t("a_propos.description"))
        self.label_auteur.configure(text=self.t("a_propos.auteur"))
