import customtkinter as ctk

from .theme import font_normal, font_sous_titre, font_titre

NAVIGATION = [
    ("accueil", "🏠  Accueil"),
    ("historique", "🕓  Historique"),
    ("parametres", "⚙️  Paramètres"),
    ("a_propos", "ℹ️  À propos"),
]


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate, on_nouvelle_recherche):
        super().__init__(parent, width=210, corner_radius=0)
        self.grid_propagate(False)
        self._on_navigate = on_navigate

        ctk.CTkLabel(self, text="🗂️ Texplorateur", font=font_titre(16)).pack(anchor='w', padx=18, pady=(28, 2))
        ctk.CTkLabel(self, text="Recherche intelligente", font=font_sous_titre(11), text_color="gray").pack(
            anchor='w', padx=18, pady=(0, 24))

        ctk.CTkButton(self, text="+ Nouvelle recherche", command=on_nouvelle_recherche, height=36).pack(
            fill='x', padx=16, pady=(0, 24))

        self._boutons = {}
        for nom, libelle in NAVIGATION:
            btn = ctk.CTkButton(
                self, text=libelle, anchor='w', fg_color="transparent",
                text_color=("gray10", "gray90"), hover_color=("gray85", "gray25"),
                font=font_normal(13), command=lambda n=nom: self._on_navigate(n),
            )
            btn.pack(fill='x', padx=10, pady=3)
            self._boutons[nom] = btn

    def definir_actif(self, nom):
        for n, btn in self._boutons.items():
            btn.configure(fg_color=("gray80", "gray28") if n == nom else "transparent")
