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
        ctk.CTkLabel(centre, text="Texplorateur", font=font_titre(22)).pack(pady=(6, 0))
        ctk.CTkLabel(centre, text=f"Version {VERSION}", font=font_sous_titre(12), text_color="gray").pack(
            pady=(0, 16))

        ctk.CTkLabel(
            centre,
            text=(
                "Recherche intelligente de phrases dans vos fichiers\n"
                ".txt, .pdf, .docx et .xlsx."
            ),
            font=font_sous_titre(13), justify="center",
        ).pack(pady=(0, 16))

        ctk.CTkLabel(centre, text="Développé par CONTRACTOR75", font=font_sous_titre(12), text_color="gray").pack()
