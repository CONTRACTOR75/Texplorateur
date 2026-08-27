import customtkinter as ctk

from .theme import font_normal, font_sous_titre, font_titre

# Les libellés viennent de i18n ("commun.<nom>") — seule l'icône est fixe.
NAVIGATION = [
    ("accueil", "🏠"),
    ("historique", "🕓"),
    ("parametres", "⚙️"),
    ("a_propos", "ℹ️"),
]


class Sidebar(ctk.CTkFrame):
    LARGEUR_ETENDUE = 210
    LARGEUR_REPLIEE = 60

    def __init__(self, parent, app, on_navigate, on_nouvelle_recherche):
        super().__init__(parent, width=self.LARGEUR_ETENDUE, corner_radius=0)
        # Les enfants sont placés avec pack() : c'est pack_propagate (pas
        # grid_propagate, qui ne concerne que des enfants gérés par grid())
        # qu'il faut désactiver pour empêcher le contenu d'imposer sa propre
        # largeur et d'écraser le width= explicite qu'on pilote au clic.
        self.pack_propagate(False)
        self.app = app
        self._on_navigate = on_navigate
        self._repliee = False

        entete = ctk.CTkFrame(self, fg_color="transparent")
        entete.pack(fill='x', padx=10, pady=(20, 4))
        self.bouton_toggle = ctk.CTkButton(
            entete, text="«", width=28, height=28, fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray85", "gray25"),
            command=self._basculer,
        )
        self.bouton_toggle.pack(side='right')

        # "Texplorateur" est le nom de l'app : pas de traduction, comme une marque.
        self.label_titre = ctk.CTkLabel(self, text="🗂️ Texplorateur", font=font_titre(16))
        self.label_titre.pack(anchor='w', padx=18, pady=(4, 2))
        self.label_sous_titre = ctk.CTkLabel(
            self, text=self.app.i18n.t("sidebar.sous_titre"), font=font_sous_titre(11), text_color="gray")
        self.label_sous_titre.pack(anchor='w', padx=18, pady=(0, 24))

        self.bouton_nouvelle_recherche = ctk.CTkButton(
            self, text=self.app.i18n.t("commun.nouvelle_recherche"), command=on_nouvelle_recherche, height=36)
        self.bouton_nouvelle_recherche.pack(fill='x', padx=16, pady=(0, 24))

        self._boutons = {}
        for nom, icone in NAVIGATION:
            btn = ctk.CTkButton(
                self, text=self._libelle_nav(nom, icone), anchor='w', fg_color="transparent",
                text_color=("gray10", "gray90"), hover_color=("gray85", "gray25"),
                font=font_normal(13), command=lambda n=nom: self._on_navigate(n),
            )
            btn.pack(fill='x', padx=10, pady=3)
            self._boutons[nom] = (btn, icone)

    def _libelle_nav(self, nom, icone):
        if self._repliee:
            return icone
        return f"{icone}  {self.app.i18n.t(f'commun.{nom}')}"

    def definir_actif(self, nom):
        for n, (btn, _) in self._boutons.items():
            btn.configure(fg_color=("gray80", "gray28") if n == nom else "transparent")

    def retraduire(self):
        self.label_sous_titre.configure(text=self.app.i18n.t("sidebar.sous_titre"))
        self.bouton_nouvelle_recherche.configure(
            text="+" if self._repliee else self.app.i18n.t("commun.nouvelle_recherche"))
        for nom, (btn, icone) in self._boutons.items():
            btn.configure(text=self._libelle_nav(nom, icone))

    def _basculer(self):
        self._repliee = not self._repliee
        self.configure(width=self.LARGEUR_REPLIEE if self._repliee else self.LARGEUR_ETENDUE)
        self.bouton_toggle.configure(text="»" if self._repliee else "«")

        if self._repliee:
            self.label_titre.pack_forget()
            self.label_sous_titre.pack_forget()
            self.bouton_nouvelle_recherche.configure(text="+")
        else:
            # `before=` réinsère les labels à leur position d'origine dans
            # l'ordre de pack, plutôt qu'à la fin (après le bouton "+").
            self.label_sous_titre.pack(anchor='w', padx=18, pady=(0, 24), before=self.bouton_nouvelle_recherche)
            self.label_titre.pack(anchor='w', padx=18, pady=(4, 2), before=self.label_sous_titre)
            self.bouton_nouvelle_recherche.configure(text=self.app.i18n.t("commun.nouvelle_recherche"))

        for nom, (btn, icone) in self._boutons.items():
            btn.configure(text=self._libelle_nav(nom, icone), anchor='center' if self._repliee else 'w')
